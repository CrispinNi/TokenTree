import os
from datetime import datetime, timedelta
from typing import List, Optional, Any
from fastapi import Depends, FastAPI, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, relationship
import httpx
from sqlalchemy import select
import asyncio
import json


# Import new modules for caching and WebSocket
from app.cache import cache
from app.websocket import manager
from app.crypto_service import CryptoService


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@db:5432/tokentree"
)

# Render provides postgres:// or postgresql://
# Convert them to async driver
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql+asyncpg://",
        1
    )

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+asyncpg://",
        1
    )

engine = create_async_engine(DATABASE_URL, echo=False, future=True)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "CHANGE_ME_SUPER_SECRET")

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


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

class TokenUpdate(BaseModel):
    quantity: float
    price_usd: float

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

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user


app = FastAPI(title="TokenTree API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://react-frontend-g87k.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await cache.init()
    await manager.init_redis()

    asyncio.create_task(price_updater())

    print("Cache, WebSocket manager, and price updater initialized")




@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Clean up cache connection on shutdown"""
    await cache.close()
    print("Cache connection closed")


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

    result = await session.execute(
        select(Token).where(Token.id == token_id, Token.user_id == current_user.id)
    )
    token = result.scalars().first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    await session.delete(token)
    await session.commit()
    return None


@app.put("/tokens/{token_id}")
async def update_token(
    token_id: int,
    token_data: TokenUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    result = await session.execute(
        select(Token).where(
            Token.id == token_id,
            Token.user_id == current_user.id
        )
    )

    token = result.scalars().first()

    if not token:
        raise HTTPException(status_code=404, detail="Token not found")

    token.quantity = token_data.quantity

    await session.commit()
    await session.refresh(token)

    return {
        "message": "Token updated successfully",
        "token_id": token.id
    }

COINGECKO_BASE = "https://api.coingecko.com/api/v3"


COIN_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "ADA": "cardano",
    "DOGE": "dogecoin",
    "XRP": "ripple",
    "DOT": "polkadot",
    "MATIC": "matic-network"
}

async def fetch_prices(symbols: List[str]) -> dict:
    if not symbols:
        return {}

    ids = [COIN_MAP.get(s.upper()) for s in symbols if COIN_MAP.get(s.upper())]

    if not ids:
        return {}

    url = f"{COINGECKO_BASE}/simple/price"
    params = {
        "ids": ",".join(ids),
        "vs_currencies": "usd"
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            print("CoinGecko rate limit hit. Sleeping 60s...")
            await asyncio.sleep(60)
        else:
            print("Price API error:", e)

        return {}

    result = {}

    for symbol in symbols:
        coin_id = COIN_MAP.get(symbol.upper())
        if coin_id and coin_id in data:
            result[symbol.upper()] = data[coin_id]["usd"]

        if result:
            await cache.set("latest_prices", result, ttl=3600)

    # ==============================
    # Store price history in Redis
    # ==============================

    now = datetime.utcnow().isoformat()

    for symbol, price in result.items():
        history_key = f"history:{symbol}"

        entry = json.dumps({
            "time": now,
            "price": price
        })

        if cache.redis:
            await cache.redis.lpush(history_key, entry)
            await cache.redis.ltrim(history_key, 0, 1439)
            await cache.redis.expire(history_key, 86400)

    return result

async def price_updater():
    await asyncio.sleep(20)  # wait for app to fully start

    while True:
        try:
            symbols = list(COIN_MAP.keys())
            print("Updating crypto prices...")

            await fetch_prices(symbols)

        except Exception as e:
            print("Price updater error:", e)

        # 30 minutes
        await asyncio.sleep(1800)
    

@app.get("/summary", response_model=TokenSummary)
async def portfolio_summary(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    result = await session.execute(select(Token).where(Token.user_id == current_user.id))
    tokens = result.scalars().all()
    symbols = list({t.symbol for t in tokens})
    prices = await get_cached_prices(symbols)
    if not prices:
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

async def get_cached_prices(symbols: List[str]) -> dict:

    prices = await cache.get("latest_prices")

    if prices:
        return {s: prices.get(s, 0) for s in symbols}

    # fallback if cache empty
    prices = await fetch_prices(symbols)
    return prices


@app.get("/charts", response_model=ChartData)
async def charts(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    result = await session.execute(
        select(Token).where(Token.user_id == current_user.id)
    )
    tokens = result.scalars().all()

    symbols = list({t.symbol for t in tokens})
    if not symbols:
        return ChartData(timeseries=[])

    points = []

    for symbol in symbols:
        if not cache.redis:
            return ChartData(timeseries=[])

        history_data = await cache.redis.lrange(f"history:{symbol}", 0, -1)

        if not history_data:
            continue

        history = [json.loads(h) for h in reversed(history_data)]

        timestamps = [h["time"] for h in history]
        prices = [h["price"] for h in history]

        points.append(
            TokenDataPoint(
            symbol=symbol,
            timestamps=timestamps,
            prices=prices
          )
        )

    return ChartData(timeseries=points)

@app.get("/news")
async def trending_news():
    """
    Crypto news endpoint with strict caching
    Prevents exceeding CryptoPanic limits
    """

    # 1️⃣ Check cache first
    cached_news = await cache.get("crypto_news")
    if cached_news:
        return cached_news

    news = []

    try:
        url = "https://cryptopanic.com/api/v1/posts/"
        params = {
            "auth_token": os.getenv("CRYPTOPANIC_API_KEY"),
            "public": "true"
        }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            for item in data.get("results", [])[:20]:
                news.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "source": item.get("source", {}).get("title"),
                    "image": None,
                    "published": item.get("published_at")
                })
        if not news:
            cached_news = await cache.get("crypto_news")
            if cached_news:
                return cached_news

    except Exception as e:
        print("News API failed:", e)

    # 2️⃣ Cache for 12 hours (21600 seconds)
    if news:
        await cache.set("crypto_news", news, ttl=43200)

    return news
# ============================================================================
# NEW ENDPOINTS: Crypto caching and WebSocket live streaming
# ============================================================================

@app.get("/api/crypto/price/{symbol}")
async def get_crypto_price(symbol: str):
    """Get current crypto price from cache or fetch fresh"""
    price_data = await CryptoService.get_price(symbol.upper())
    if not price_data:
        raise HTTPException(status_code=404, detail="Crypto not found")
    return price_data


@app.get("/api/crypto/prices")
async def get_crypto_prices(symbols: str):
    """Get multiple crypto prices (comma-separated symbols)"""
    symbol_list = [s.strip().upper() for s in symbols.split(",")]
    return await CryptoService.get_prices_bulk(symbol_list)


@app.post("/api/crypto/refresh")
async def refresh_crypto_prices(symbols: List[str]):
    """Manually trigger background job to update prices"""
    CryptoService.trigger_price_update(symbols)
    return {"status": "triggered", "symbols": symbols}


@app.websocket("/ws/price/{symbol}")
async def websocket_price_endpoint(websocket: WebSocket, symbol: str):
    """WebSocket endpoint for streaming live crypto prices"""
    symbol = symbol.upper()
    await manager.connect(websocket, symbol)
    
    try:
        # Subscribe to Redis pub/sub for this symbol
        pubsub_task = asyncio.create_task(manager.subscribe_to_updates(symbol))
        
        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            # Echo back ping/pong if needed
            await websocket.send_text(json.dumps({"type": "ping", "data": data}))
    
    except WebSocketDisconnect:
        await manager.disconnect(websocket, symbol)
        print(f"Client disconnected from {symbol}")
    except Exception as e:
        await manager.disconnect(websocket, symbol)
        print(f"WebSocket error for {symbol}: {e}")
                
    


@app.get("/")
async def root():
    return {"status": "ok", "message": "TokenTree API"}