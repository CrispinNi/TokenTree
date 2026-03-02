import os
from datetime import datetime, timedelta
from typing import List, Optional, Any

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, relationship
import httpx


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+aiomysql://tokentree:tokentree_pw@db:3306/tokentree",
)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "CHANGE_ME_SUPER_SECRET")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    symbol = Column(String(20), nullable=False)
    quantity = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="tokens")


class TokenBase(BaseModel):
    symbol: str
    quantity: float


class TokenCreate(TokenBase):
    pass


class TokenRead(TokenBase):
    id: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class TokenSummary(BaseModel):
    total_usd_value: float
    per_token: List[dict]


class TokenDataPoint(BaseModel):
    symbol: str
    timestamps: List[str]
    prices: List[float]


class ChartData(BaseModel):
    timeseries: List[TokenDataPoint]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class LoginResponse(TokenResponse):
    user: UserRead


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    # bcrypt backend used by passlib only supports up to 72 bytes;
    # truncate to avoid runtime errors on very long passwords.
    return pwd_context.hash(password[:72])


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    from sqlalchemy import select

    result = await session.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id: int = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise credentials_exception

    from sqlalchemy import select

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user


app = FastAPI(title="TokenTree API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/auth/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    existing = await get_user_by_email(session, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=get_password_hash(payload.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@app.post("/auth/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserRead.model_validate(user),
    )


@app.get("/me", response_model=UserRead)
async def read_me(current_user: User = Depends(get_current_user)):
    return UserRead.model_validate(current_user)


@app.get("/tokens", response_model=List[TokenRead])
async def list_tokens(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    from sqlalchemy import select

    result = await session.execute(
        select(Token).where(Token.user_id == current_user.id).order_by(Token.created_at.desc())
    )
    tokens = result.scalars().all()
    return [TokenRead.model_validate(t) for t in tokens]


@app.post("/tokens", response_model=TokenRead, status_code=status.HTTP_201_CREATED)
async def add_token(
    payload: TokenCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    token = Token(
        user_id=current_user.id,
        symbol=payload.symbol.upper(),
        quantity=payload.quantity,
    )
    session.add(token)
    await session.commit()
    await session.refresh(token)
    return TokenRead.model_validate(token)


@app.delete("/tokens/{token_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_token(
    token_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    from sqlalchemy import select

    result = await session.execute(
        select(Token).where(Token.id == token_id, Token.user_id == current_user.id)
    )
    token = result.scalars().first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    await session.delete(token)
    await session.commit()
    return None


COINGECKO_BASE = "https://api.coingecko.com/api/v3"


async def fetch_prices(symbols: List[str]) -> dict:
    if not symbols:
        return {}

    ids = ",".join(s.lower() for s in symbols)
    url = f"{COINGECKO_BASE}/simple/price"
    params = {"ids": ids, "vs_currencies": "usd"}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        # On any pricing API error (429 rate limit, network, etc.), fall back to zero prices
        return {}

    return {k.upper(): v.get("usd", 0.0) for k, v in data.items()}


@app.get("/summary", response_model=TokenSummary)
async def portfolio_summary(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    from sqlalchemy import select

    result = await session.execute(select(Token).where(Token.user_id == current_user.id))
    tokens = result.scalars().all()
    symbols = list({t.symbol for t in tokens})
    prices = await fetch_prices(symbols)

    per_token = []
    total = 0.0
    for t in tokens:
        price = prices.get(t.symbol.upper(), 0.0)
        value = price * t.quantity
        total += value
        per_token.append(
            {
                "id": t.id,
                "symbol": t.symbol,
                "quantity": t.quantity,
                "price_usd": price,
                "value_usd": value,
            }
        )

    return TokenSummary(total_usd_value=total, per_token=per_token)


@app.get("/charts", response_model=ChartData)
async def charts(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    from sqlalchemy import select

    result = await session.execute(select(Token).where(Token.user_id == current_user.id))
    tokens = result.scalars().all()
    symbols = list({t.symbol for t in tokens})
    if not symbols:
        return ChartData(timeseries=[])

    end = int(datetime.utcnow().timestamp())
    start = end - 60 * 60 * 24

    async with httpx.AsyncClient(timeout=10) as client:
        points: List[TokenDataPoint] = []
        for symbol in symbols:
            coin_id = symbol.lower()
            url = f"{COINGECKO_BASE}/coins/{coin_id}/market_chart/range"
            params = {"vs_currency": "usd", "from": start, "to": end}
            try:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()
                prices = data.get("prices", [])
                timestamps = [
                    datetime.utcfromtimestamp(p[0] / 1000).isoformat() for p in prices
                ]
                values = [float(p[1]) for p in prices]
                points.append(
                    TokenDataPoint(symbol=symbol.upper(), timestamps=timestamps, prices=values)
                )
            except Exception:
                continue

    return ChartData(timeseries=points)


@app.get("/news")
async def trending_news():
    url = "https://min-api.cryptocompare.com/data/v2/news/"
    params = {"lang": "EN"}
    headers = {}
    api_key = os.getenv("CRYPTOCOMPARE_API_KEY")
    if api_key:
        headers["authorization"] = f"Apikey {api_key}"

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params, headers=headers)
            resp.raise_for_status()
            data = resp.json().get("Data", [])
    except Exception:
        return []

    items: List[dict] = []
    for item in data[:20]:
        items.append(
            {
                "title": item.get("title", ""),
                "url": str(item.get("url", "")),
                "source": item.get("source", None),
                "published_at": item.get("published_on"),
            }
        )
    return items


@app.get("/")
async def root():
    return {"status": "ok", "message": "TokenTree API"}

