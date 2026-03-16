import os
import ssl
from celery import Celery
from datetime import timedelta

# Redis URL from environment (Upstash uses rediss://)
redis_url = os.getenv("REDIS_URL")

broker_url = os.getenv("CELERY_BROKER_URL", redis_url)
backend_url = os.getenv("CELERY_RESULT_BACKEND", redis_url)

# Initialize Celery
app = Celery(
    "tokentree",
    broker=broker_url,
    backend=backend_url
)

# Celery configuration
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# 🔐 Required for Upstash / TLS Redis
if broker_url and broker_url.startswith("rediss://"):
    app.conf.broker_use_ssl = {
        "ssl_cert_reqs": ssl.CERT_NONE
    }

if backend_url and backend_url.startswith("rediss://"):
    app.conf.redis_backend_use_ssl = {
        "ssl_cert_reqs": ssl.CERT_NONE
    }

# Schedule periodic tasks
app.conf.beat_schedule = {
    "fetch-crypto-prices-every-5-min": {
        "task": "app.tasks.fetch_and_cache_prices",
        "schedule": timedelta(minutes=5),
        "args": (["BTC", "ETH", "BNB", "XRP", "ADA", "SOL", "DOT", "MATIC"],)
    },
}

# Import tasks for registration
from app import tasks