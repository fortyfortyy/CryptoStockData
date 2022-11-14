import os

from django.conf import settings
from stocks.utils import fetch_data_from_url, extract_data_from_url

import redis
from celery import Celery

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockapp.settings')

app = Celery('stockapp')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


# We used CELERY_BROKER_URL in settings.py instead of:
# app.conf.broker_url = ''

# We used CELERY_BEAT_SCHEDULER in settings.py instead of:
# app.conf.beat_scheduler = ''django_celery_beat.schedulers.DatabaseScheduler


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls get_stock_prices_task every 5 seconds.
    sender.add_periodic_task(5.0, get_stock_prices_task.s(), name='stock_data')


REDIS_INSTANCE = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=1)

CRYPTO_API_KEY = settings.CRYPTO_API_KEY

@app.task
def get_stock_prices_task():
    headers = {
        'authorization': CRYPTO_API_KEY
    }
    urls_to_check = [
        'https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH,DOME,BNB,SOL,FTT&tsyms=USD'
    ]

    for url in urls_to_check:
        fetch_data = fetch_data_from_url(url, headers)
        if fetch_data is None:
            continue

        extract_data = extract_data_from_url(fetch_data)
        for stock_name, values in extract_data.items():
            REDIS_INSTANCE.set(stock_name, str(values))

    print('Dava has been saved on Redis!')
