from celery import shared_task
from .models import Task
from .coinmarketcap import CoinMarketCap
import logging

logger = logging.getLogger(__name__)
scraper = CoinMarketCap()

@shared_task
def scrape_coin_data(task_id, coin):
    try:
        task = Task.objects.get(id=task_id)
        logger.info('Scraping data for coin: %s', coin)
        data = scraper.getData(name=coin)
        task.status = 'COMPLETED'
        task.data = data
    except Exception as e:
        logger.error('Failed to scrape data for coin %s: %s', coin, e)
        task.status = 'FAILED'
        task.data = {'error': str(e)}
    task.save()

