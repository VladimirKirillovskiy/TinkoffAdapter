from TinkoffAdapter.settings import SANDBOX_TOKEN
from django.core.management.base import BaseCommand
import logging
import tinvest as ti
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from time import sleep


logger = logging.getLogger('root')

stocks_map = {
    'BBG000BWPXQ8': {
        'required_price': Decimal(38),
        'trend': 'up',
    },
    'BBG004731489': {
        'required_price': Decimal(26000),
        'trend': 'down',
    },
    'BBG004S685M3': {
        'required_price': Decimal(80),
        'trend': 'down',
    },
    'BBG00475K2X9': {
        'required_price': Decimal(1),
        'trend': 'up',
    },
}


def del_stock(figi):
    del stocks_map[figi]


def check_stocks():
    client = ti.SyncClient(SANDBOX_TOKEN, use_sandbox=True)
    to = datetime.now(tz=timezone.utc)
    from_ = to - timedelta(days=1)
    interval = ti.CandleResolution('1min')

    result = {}

    for figi in stocks_map:
        try:
            response = client.get_market_candles(figi, from_, to, interval)
            if response.payload.candles != []:
                current_price = response.payload.candles[-1].c
            else:
                continue

            if ((current_price >= stocks_map[figi]['required_price'] and stocks_map[figi]['trend'] == 'up') or
                    (current_price <= stocks_map[figi]['required_price'] and stocks_map[figi]['trend'] == 'down')):
                result[figi] = current_price

        except (ti.exceptions.BadRequestError, ti.exceptions.UnexpectedError) as exception:
            logger.error(exception)

        except ti.exceptions.TooManyRequestsError as exception:
            sleep(1)
            logger.error(exception)

    for figi in result:
        del_stock(figi)

    print(result)
    return result


class Command(BaseCommand):
    def handle(self, *args, **options):
        check_stocks()