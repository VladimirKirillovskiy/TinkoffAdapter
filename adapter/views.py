from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from TinkoffAdapter.settings import SANDBOX_TOKEN
import tinvest as ti
from tinvest.exceptions import UnexpectedError
import yfinance as yf
import adapter.services as services
import logging


logger = logging.getLogger('root')

response_sample = {
    'code': 200,
    'detail': 'ok',
    'payload': [],
    'total': 0,
}


class MarketStocksList(APIView):
    """

    Получение списка акций

    Parameters
    ----------

    """
    permission_classes = [AllowAny, ]

    def get(self, request):
        r = response_sample.copy()
        try:
            client = ti.SyncClient(SANDBOX_TOKEN, use_sandbox=True)
            response = client.get_market_stocks().dict()['payload']
            stocks = response['instruments']

            for item in stocks:
                res = {
                    'name': item['name'],
                    'ticker': item['ticker'],
                    'currency': item['currency'],
                }
                r['payload'].append(res)

            r['total'] = int(response['total'])

        except UnexpectedError as e:
            logger.warning('marketall: ' + e.text)
            r['code'] = 500
            r['detail'] = eval(e.text)['payload']['code']

        return Response(r)


class MarketStocksDetail(APIView):

    """
    
    Получение инструмента по тикеру

    Parameters
    ----------
    
    **ticker** : string
        Описание переменной: название тикера

    """
    permission_classes = [AllowAny, ]

    def get(self, request, ticker):
        r = response_sample.copy()
        try:
            client = ti.SyncClient(SANDBOX_TOKEN, use_sandbox=True)
            response = client.get_market_search_by_ticker(ticker).dict()['payload']

            if response['total'] != 0:
                response = response['instruments'][0]
                data_price = client.get_market_orderbook(response['figi'], 0)
                response['last_price'] = data_price.dict()['payload']['last_price']
                r['payload'] = [response]
                r['total'] = len(r['payload'])

            else:
                logger.warning('marketstock: invalid ticker')
                r['code'] = '500'
                r['detail'] = 'invalid ticker'

        except UnexpectedError as e:
            logger.warning('marketstock: ' + e.text)
            r['code'] = 500
            r['detail'] = eval(e.text)['payload']['code']

        return Response(r)


class MarketCurrenciesList(APIView):
    """
    
    Получение списка валютных пар
    
    Parameters
    ----------

    
    """

    permission_classes = [AllowAny, ]
    
    def get(self, request):
        r = response_sample.copy()
        try:
            client = ti.SyncClient(SANDBOX_TOKEN, use_sandbox=True)
            data = client.get_market_currencies().dict()['payload']['instruments']
            data_json = []

            for item in data:
                data_price = client.get_market_orderbook(item['figi'], 0)
                res = {
                    'name': item['name'],
                    'ticker': item['ticker'],
                    'currency': item['currency'],
                    'last_price': data_price.dict()['payload']['last_price']
                }
                data_json.append(res)

            r['payload'] = data_json
            r['total'] = len(r['payload'])

        except UnexpectedError as e:
            logger.warning('currencies_list: ' + e.text)
            r['code'] = 500
            r['detail'] = eval(e.text)['payload']['code']

        return Response(r)


class MarketCurrenciesDetail(APIView):
    """
    
    Получение валютных пар по названию валюты

    Parameters
    ----------
    **currency** : string
        Описание переменной: название валюты

    """
    permission_classes = [AllowAny, ]

    def get(self, request, currency):
        r = response_sample.copy()
        try:
            client = ti.SyncClient(SANDBOX_TOKEN, use_sandbox=True)
            data = client.get_market_currencies().dict()['payload']['instruments']
            data_json = []

            for item in data:
                if item["ticker"][:3] == currency.upper():
                    data_price = client.get_market_orderbook(item['figi'], 0)
                    item['last_price'] = data_price.dict()['payload']['last_price']
                    data_json += [item]

            if len(data_json) != 0:
                r['payload'] = data_json
                r['total'] = len(r['payload'])
            else:
                logger.warning('currencies_detail: invalid ticker')
                r['code'] = '500'
                r['detail'] = 'invalid ticker'

        except UnexpectedError as e:
            logger.warning('currencies_detail: ' + e.text)
            r['code'] = 500
            r['detail'] = eval(e.text)['payload']['code']

        return Response(r)


class QuartEarnings(APIView):
    """
    
    Получение списка квартальной прибыли по тикеру

    Parameters
    ----------
    **ticker** : string
        Описание переменной: название тикера
    
    """ 
    permission_classes = [AllowAny, ]

    def get(self, request, ticker):
        tick = yf.Ticker(ticker)
        data = tick.quarterly_earnings
        r = response_sample.copy()
        data_json = []

        if data is not None:
            data_json.append(data.to_dict(orient='index'))
            r['payload'] = data_json
            r['total'] = len(r['payload'])

        return Response(r)


class Info(APIView):
    """
    
    Получение информации по тикеру

    Parameters
    ----------
    **ticker** : string
        Описание переменной: название тикера
    
    """    
    permission_classes = [AllowAny, ]

    def get(self, request, ticker):
        tick = yf.Ticker(ticker)
        data = tick.info
        r = response_sample.copy()

        if len(data) > 2:
            if data['trailingEps'] != None:
                EPS = round(data['trailingEps'], 2)
            else:
                EPS = None
            if data['beta'] != None:
                Beta = round(data['beta'], 2)
            else:
                Beta = None
            if data['debtToEquity'] != None:
                DebtToEquity = round(data['debtToEquity'], 2)
            else:
                DebtToEquity = None
            data_json = {
                'MarketCap': data['marketCap'],
                'SharesOutstanding': data['sharesOutstanding'],
                'Revenue': data['totalRevenue'],
                'EPS': EPS,
                'Beta': Beta,
                'Cash': data['totalCash'],
                'Debt': data['totalDebt'],
                'DebtToEquity': DebtToEquity
            }
            r['payload'] = [data_json]
            r['total'] = len(r['payload'])

        return Response(r)


class Dividends(APIView):
    """
    
    Получение списка дивидендов по тикету

    Parameters
    ----------
    **ticker** : string
        Описание переменной: название тикера
    
    """ 

    permission_classes = [AllowAny, ]

    def get(self, request, ticker):
        tick = yf.Ticker(ticker)
        data = tick.dividends
        r = response_sample.copy()
        data_json = []

        if len(data) > 0:
            data = data.to_dict()

            for item in data:
                res = {
                    'data': item.value // 10 ** 9,
                    'value': data[item],
                }
                data_json.append(res)

        r['payload'] = data_json
        r['total'] = len(r['payload'])

        return Response(r)


class NextDivs(APIView):
    """
    
    Получение следующего дивиденда по тикету

    Parameters
    ----------
    **ticker** : string
        Описание переменной: название тикера
    
    """ 
    permission_classes = [AllowAny, ]

    def get(self, request, ticker):
        tick = yf.Ticker(ticker)
        data = tick.info
        r = response_sample.copy()

        if len(data) > 2:
            time = data['exDividendDate']
            data_json = {'next_div_day': time}
            r['payload'] = [data_json]
            r['total'] = len(r['payload'])

        return Response(r)


class NextEarns(APIView):
    """
    
    Получение следующей прибыли по тикету

    Parameters
    ----------
    **ticker** : string
        Описание переменной: название тикера
    
    """
    permission_classes = [AllowAny, ]

    def get(self, request, ticker):
        tick = yf.Ticker(ticker)
        data = tick.calendar
        r = response_sample.copy()
        
        if data is not None:
            col = data.columns.values[1]
            data_json = {
              'Date': data.loc[data.index.values[0], col].value // 10 ** 9,
              'EPS': data.loc[data.index.values[1], col],
              'Revenue': data.loc[data.index.values[4], col],
            }
           
            r['payload'] = [data_json]
            r['total'] = len(r['payload'])

        return Response(r)


class Insiders(APIView):
    """
    
    Получение инсайдерской информации по тикету или по тикету/периода времени 

    Parameters
    ----------
    **ticker** : string
        Описание переменной: название тикера

    (*optional*) **days** : integer
        Описание переменной: количество дней (по умолчанию 10)
    
    """    
    permission_classes = [AllowAny,]

    def get(self, request, ticker, days=10):
        r = response_sample.copy()
        data = services.get_insiders(r, ticker, days)
        return Response(services.pd_insiders(data))


class SandboxAccountRegister(APIView):
    """
    
    Регистрация токена из "песочницы"

    Parameters
    ----------
    **sandbox_token** : string
        Описание переменной: токен песочницы
    
    """ 
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        r = response_sample.copy()

        if 'sandbox_token' in data:
            try:
                client = ti.SyncClient(data['sandbox_token'], use_sandbox=True)
                response = client.register_sandbox_account(ti.SandboxRegisterRequest.tinkoff())
                r['payload'] = [{
                    'broker_account_id': response.payload.broker_account_id
                }]

            except UnexpectedError:
                logger.warning('sandbox_register: invalid sandbox_token')
                r['code'] = 401
                r['detail'] = 'invalid sandbox_token'

        else:
            logger.warning('sandbox_register: lack of data. post sandbox_token')
            r['code'] = 400
            r['detail'] = 'lack of data. post sandbox_token'

        return Response(r)


class SandboxAccountRemove(APIView):
    """
    
    Удаление счёта из "песочницы"

    Parameters
    ----------
    **sandbox_token** : string
        Описание переменной: токен песочницы
    
    """ 
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        r = response_sample.copy()

        if 'sandbox_token' in data:
            try:
                client = ti.SyncClient(data['sandbox_token'], use_sandbox=True)
                accounts = client.get_accounts().payload.accounts

                if accounts[0].broker_account_type == 'Tinkoff':
                    client.remove_sandbox_account(accounts[0].broker_account_id)
                else:
                    logger.warning('sandbox_remove: account not registered')
                    r['code'] = '500'
                    r['detail'] = 'account not registered'

            except UnexpectedError:
                logger.warning('sandbox_remove: invalid sandbox_token')
                r['code'] = 401
                r['detail'] = 'invalid sandbox_token'

        else:
            logger.warning('sandbox_remove: lack of data. post sandbox_token')
            r['code'] = 400
            r['detail'] = 'lack of data. post sandbox_token'

        return Response(r)


class SandboxAccountClear(APIView):
    """
    
    Удаление всех позиций из "песочницы"

    Parameters
    ----------
    **sandbox_token** : string
        Описание переменной: токен песочницы
    
    """
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        r = response_sample.copy()

        if 'sandbox_token' in data:
            try:
                client = ti.SyncClient(data['sandbox_token'], use_sandbox=True)
                accounts = client.get_accounts().payload.accounts

                if accounts[0].broker_account_type == 'Tinkoff':
                    client.clear_sandbox_account(accounts[0].broker_account_id)
                else:
                    logger.warning('sandbox_clear: account not registered')
                    r['code'] = '500'
                    r['detail'] = 'account not registered'

            except UnexpectedError:
                logger.warning('sandbox_clear: invalid sandbox_token')
                r['code'] = 401
                r['detail'] = 'invalid sandbox_token'

        else:
            logger.warning('sandbox_clear: lack of data. post sandbox_token')
            r['code'] = 400
            r['detail'] = 'lack of data. post sandbox_token'

        return Response(r)


class SandboxSetStocks(APIView):
    """

    Выставление баланса по инструметным позициям

    Parameters
    ----------
    **sandbox_token** : string
        Описание переменной: токен песочницы

    **ticker** : string
        Описание переменной: определение тикера

    **balance** : decimal
        Описание переменной: определение баланса
    """

    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        r = response_sample.copy()

        if ('sandbox_token' in data) and ('ticker' in data) and ('balance' in data):
            try:
                client = ti.SyncClient(data['sandbox_token'], use_sandbox=True)
                accounts = client.get_accounts().payload.accounts

                if accounts[0].broker_account_type == 'Tinkoff':
                    broker_account_id = accounts[0].broker_account_id
                    figi = client.get_market_search_by_ticker(data['ticker']).payload.dict()

                    if figi['total'] != 0:
                        body = ti.SandboxSetPositionBalanceRequest(
                            balance=data['balance'],
                            figi=figi['instruments'][0]['figi'],
                        )
                        client.set_sandbox_positions_balance(body, broker_account_id)
                    else:
                        logger.warning('sandbox_stock: invalid ticker')
                        r['code'] = '500'
                        r['detail'] = 'invalid ticker'

                else:
                    logger.warning('sandbox_stock: account not registered')
                    r['code'] = '500'
                    r['detail'] = 'account not registered'

            except UnexpectedError:
                logger.warning('sandbox_stock: invalid sandbox_token')
                r['code'] = 401
                r['detail'] = 'invalid sandbox_token'

        else:
            logger.warning('sandbox_stock: lack of data. post sandbox_token, ticker, balance')
            r['code'] = 400
            r['detail'] = 'lack of data. post sandbox_token, ticker, balance'

        return Response(r)


class SandboxSetCurrencies(APIView):
    """

    Выставление баланса по валютным позициям из "песочницы"

    Parameters
    ----------
    **sandbox_token** : string
        Описание переменной: токен песочницы

    **currency** : string
        Описание переменной: определение тикера валюты

    **balance** : decimal
        Описание переменной: определение баланса
    """

    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        r = response_sample.copy()

        if ('sandbox_token' in data) and ('currency' in data) and ('balance' in data):
            try:
                client = ti.SyncClient(data['sandbox_token'], use_sandbox=True)
                accounts = client.get_accounts().payload.accounts

                if accounts[0].broker_account_type == 'Tinkoff':
                    broker_account_id = accounts[0].broker_account_id
                    if data['currency'] in ['RUB', 'EUR', 'USD']:
                        body = ti.SandboxSetCurrencyBalanceRequest(
                            balance=data['balance'],
                            currency=data['currency'],
                        )
                        client.set_sandbox_currencies_balance(body, broker_account_id)
                    else:
                        logger.warning('sandbox_currency: invalid currency')
                        r['code'] = '500'
                        r['detail'] = 'invalid currency'

                else:
                    logger.warning('sandbox_currency: account not registered')
                    r['code'] = '500'
                    r['detail'] = 'account not registered'

            except UnexpectedError:
                logger.warning('sandbox_currency: invalid sandbox_token')
                r['code'] = 401
                r['detail'] = 'invalid sandbox_token'

        else:
            logger.warning('sandbox_currency: lack of data. post sandbox_token, currency, balance')
            r['code'] = 400
            r['detail'] = 'lack of data. post sandbox_token, currency, balance'

        return Response(r)


class CheckPortfolioStocks(APIView):
    """
    
    Получение портфеля клиента

    Parameters
    ----------
    **sandbox_token** : string
        Описание переменной: токен песочницы
    
    """    
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        r = response_sample.copy()

        if 'sandbox_token' in data:
            try:
                client = ti.SyncClient(data['sandbox_token'], use_sandbox=True)
                accounts = client.get_accounts().payload.accounts

                if accounts[0].broker_account_type == 'Tinkoff':
                    broker_account_id = accounts[0].broker_account_id
                    r['payload'] = [dict(item) for item
                                    in client.get_portfolio(broker_account_id).payload.positions]
                    r['total'] = len(r['payload'])
                else:
                    logger.warning('sandbox_stocks: account not registered')
                    r['code'] = '500'
                    r['detail'] = 'account not registered'

            except UnexpectedError:
                logger.warning('sandbox_stocks: invalid sandbox_token')
                r['code'] = 401
                r['detail'] = 'invalid sandbox_token'

        else:
            logger.warning('sandbox_stocks: lack of data. post sandbox_token')
            r['code'] = 400
            r['detail'] = 'lack of data. post sandbox_token'
            
        return Response(r)


class CheckPortfolioCurrencies(APIView):
    """
    
    Получение валютных активов клиента

    Parameters
    ----------
    **sandbox_token** : string
        Описание переменной: токен песочницы
    
    """
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        r = response_sample.copy()

        if 'sandbox_token' in data:
            try:
                client = ti.SyncClient(data['sandbox_token'], use_sandbox=True)
                accounts = client.get_accounts().payload.accounts

                if accounts[0].broker_account_type == 'Tinkoff':
                    broker_account_id = accounts[0].broker_account_id
                    r['payload'] = [dict(item) for item
                                    in client.get_portfolio_currencies(broker_account_id).payload.currencies]
                    r['total'] = len(r['payload'])
                else:
                    logger.warning('sandbox_currencies: account not registered')
                    r['code'] = '500'
                    r['detail'] = 'account not registered'

            except UnexpectedError:
                logger.warning('sandbox_currencies: invalid sandbox_token')
                r['code'] = 401
                r['detail'] = 'invalid sandbox_token'

        else:
            logger.warning('sandbox_currencies: lack of data. post sandbox_token')
            r['code'] = 400
            r['detail'] = 'lack of data. post sandbox_token'

        return Response(r)


class StocksMarketOrder(APIView):
    """
    
    Создание рыночной заявки по акциям

    Parameters
    ----------
    **sandbox_token** : string
        Описание переменной: токен песочницы

    **ticker** : string
        Описание переменной: определение тикера

    **lots** : integer
        Описание переменной: определение лотов

    **operation** : string ("Buy", "Sell")
        Описание переменной: определение операции
    
    """
    
    permission_classes = [AllowAny, ]

    # Сначала смотрится текущая цена, потом создается лимитная заявка по текущей цене.
    # Потому что в Sandbox "Все рыночные поручения исполняются по фиксированной цене в 100"

    def post(self, request):
        data = request.data
        r = response_sample.copy()

        if ('sandbox_token' in data) and ('ticker' in data) and ('lots' in data) and ('operation' in data):
            try:
                client = ti.SyncClient(data['sandbox_token'], use_sandbox=True)
                accounts = client.get_accounts().payload.accounts

                if accounts[0].broker_account_type == 'Tinkoff':
                    broker_account_id = accounts[0].broker_account_id
                    info = client.get_market_search_by_ticker(data['ticker']).dict()['payload']

                    if info['total'] != 0:
                        figi = info['instruments'][0]['figi']
                        data_price = client.get_market_orderbook(figi, 0)
                        price = data_price.payload.last_price
                        body = ti.LimitOrderRequest(
                            lots=data['lots'],
                            operation=data['operation'],
                            price=price,
                        )
                        try:
                            client.post_orders_limit_order(figi, body, broker_account_id)
                            r['payload'] = [dict(item) for item
                                            in client.get_portfolio(broker_account_id).payload.positions]
                            r['total'] = len(r['payload'])

                        except UnexpectedError as e:
                            logger.warning('sandbox_stocks_market_order: ' + e.text)
                            r['code'] = 500
                            r['detail'] = eval(e.text)['payload']['code']
                    else:
                        logger.warning('sandbox_stocks_market_order: invalid ticker')
                        r['code'] = '500'
                        r['detail'] = 'invalid ticker'
                else:
                    logger.warning('sandbox_stocks_market_order: account not registered')
                    r['code'] = '500'
                    r['detail'] = 'account not registered'

            except UnexpectedError:
                logger.warning('sandbox_stocks_market_order: invalid sandbox_token')
                r['code'] = 401
                r['detail'] = 'invalid sandbox_token'

        else:
            logger.warning('sandbox_stocks_market_order: lack of data. post sandbox_token, ticker, lots, operation')
            r['code'] = 400
            r['detail'] = 'lack of data. post sandbox_token, ticker, lots, operation'

        return Response(r)


class CurrenciesMarketOrder(APIView):
    """
    
    Создание рыночной заявки по валюте

    Parameters
    ----------
    **sandbox_token** : string
        Описание переменной: токен песочницы

    **ticker** : string
        Описание переменной: определение тикера

    **lots** : integer
        Описание переменной: определение лотов

    **operation** : string ("Buy", "Sell")
        Описание переменной: определение операции
    
    """
    permission_classes = [AllowAny, ]

    # 1 лот = 2000 единиц валюты
    # Сначала смотрится текущая цена, потом создается лимитная заявка по текущей цене.
    # Потому что в Sandbox "Все рыночные поручения исполняются по фиксированной цене в 100"

    def post(self, request):
        data = request.data
        r = response_sample.copy()

        if ('sandbox_token' in data) and ('ticker' in data) and ('lots' in data) and ('operation' in data):
            try:
                client = ti.SyncClient(data['sandbox_token'], use_sandbox=True)
                accounts = client.get_accounts().payload.accounts

                if accounts[0].broker_account_type == 'Tinkoff':
                    broker_account_id = accounts[0].broker_account_id
                    info = client.get_market_currencies().dict()['payload']['instruments']
                    figi = None

                    for item in info:
                        if item["ticker"][:3] == data['ticker'].upper():
                            figi = item['figi']

                        if figi is not None:
                            data_price = client.get_market_orderbook(item['figi'], 0)
                            price = data_price.payload.last_price
                            body = ti.LimitOrderRequest(
                                lots=data['lots'],
                                operation=data['operation'],
                                price=price,
                            )
                            try:
                                client.post_orders_limit_order(figi, body, broker_account_id)
                                r['payload'] = [dict(item) for item
                                                in client.get_portfolio(broker_account_id).payload.positions]
                                r['total'] = len(r['payload'])
                            except UnexpectedError as e:
                                logger.warning('currencies_market_order: '+ e.text)
                                r['code'] = '500'
                                r['detail'] = eval(e.text)['payload']['code']
                        else:
                            logger.warning('currencies_market_order: invalid ticker')
                            r['code'] = '500'
                            r['detail'] = 'invalid ticker'
                else:
                    logger.warning('currencies_market_order: account not registered')
                    r['code'] = '500'
                    r['detail'] = 'account not registered'

            except UnexpectedError:
                logger.warning('currencies_market_order: invalid sandbox_token')
                r['code'] = 401
                r['detail'] = 'invalid sandbox_token'
        else:
            logger.warning('currencies_market_order: lack of data. post sandbox_token, ticker, lots, operation')
            r['code'] = 400
            r['detail'] = 'lack of data. post sandbox_token, ticker, lots, operation'

        return Response(r)


class NewsSentiment(APIView):
    """
    
    Получение анализа новостей на предмет движения рынка по тикету

    Parameters
    ----------
    **ticker** : string
        Описание переменной: определение тикера
    
    """
    permission_classes = [AllowAny, ]

    def get(self, request, ticker):
        r = response_sample.copy()
        data = services.get_news_sentiment(r, ticker.upper())

        return Response(data)


class NewsCompany(APIView):
    """
    
    Получение анализа новостей на предмет движения рынка по тикету

    Parameters
    ----------
    **ticker** : string
        Описание переменной: определение тикера

    (*optional*) **days** : integer
        Описание переменной: количество дней (по умолчанию 10)
    
    """
    permission_classes = [AllowAny, ]

    def get(self, request, ticker, days=10):
        r = response_sample.copy()
        data = services.get_news_company(r, ticker.upper(), days)

        return Response(data)


class Recommendations(APIView):
    """
    
    Получение рекомендаций из новостей по тикету

    Parameters
    ----------
    **ticker** : string
        Описание переменной: определение тикера
    
    """
    permission_classes = [AllowAny, ]

    def get(self, request, ticker):
        r = response_sample.copy()
        data = services.get_recommendations(r, ticker)
        return Response(data)

    # Поля ответа:
    # 'date' - дата рекоммендации,
    # 'firm' - компания, давшая рекоммендацию,
    # 'to_grade' - рекоммендация изменена на,
    # 'from_grade' - рекоммендация изменена с,
    # 'action' - суть изменения рекоммендации(повышена, понижена, добавлена).


class RecommendationsInDays(APIView):
    """
    
    Получение ремомендаций из новостей по тикету и дате

    Parameters
    ----------
    **ticker** : string
        Описание переменной: определение тикера
    
    """
    permission_classes = [AllowAny, ]

    def get(self, request, ticker, days=10):
        r = response_sample.copy()
        data = services.get_recommendations_days(r, ticker, days)
        return Response(data)

    # Поля ответа:
    # 'date' - дата рекоммендации,
    # 'firm' - компания, давшая рекоммендацию,
    # 'to_grade' - рекоммендация изменена на,
    # 'from_grade' - рекоммендация изменена с,
    # 'action' - суть изменения рекоммендации(повышена, понижена, добавлена).


class MajorHolders(APIView):
    """
    
    Получение информации об акции по тикету

    Parameters
    ----------
    **ticker** : string
        Описание переменной: определение тикера
    
    """
    permission_classes = [AllowAny, ]

    def get(self, request, ticker):
        r = response_sample.copy()
        data = services.get_major_holders(r, ticker)
        return Response(data)

    # Поля ответа:
    # 'holder' - компания держатель акций,
    # 'shares' - количество акций в руках компании,
    # 'date_reported' - дата последнего отчёта, по которому берутся данные,
    # '%out' - процент от всех акций,
    # 'value' - общая стоимость акций,
