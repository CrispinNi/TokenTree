import os
from celery import Celery
from celery.schedules import schedule
from datetime import timedelta

# Initialize Celery
app = Celery(
    'tokentree',
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")
)

# Celery configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Schedule periodic tasks
app.conf.beat_schedule = {
    'fetch-crypto-prices-every-5-min': {
        'task': 'app.tasks.fetch_and_cache_prices',
        'schedule': timedelta(minutes=5),
        'args': (['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'SOL', 'DOT', 'MATIC'],)
    },
}

# Import tasks for registration
from app import tasks