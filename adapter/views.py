from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from TinkoffAdapter.settings import SANDBOX_TOKEN
import tinvest as ti
from tinvest.exceptions import UnexpectedError
import yfinance as yf
import adapter.services as services


response_sample = {
    'code': 200,
    'detail': '',
    'payload': [],
    'total': 0,
}


class MarketStocksList(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        client = ti.SyncClient(SANDBOX_TOKEN, use_sandbox=True)
        register = client.register_sandbox_account(ti.SandboxRegisterRequest.tinkoff())
        response = client.get_market_stocks().dict()['payload']
        stocks = response['instruments']
        r = response_sample.copy()

        for item in stocks:
            res = {
                'name': item['name'],
                'ticker': item['ticker'],
                'currency': item['currency'],
            }
            r['payload'].append(res)

        r['total'] = int(response['total'])

        return Response(r)


class MarketStocksDetail(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, ticker):
        client = ti.SyncClient(SANDBOX_TOKEN, use_sandbox=True)
        register = client.register_sandbox_account(ti.SandboxRegisterRequest.tinkoff())
        response = client.get_market_search_by_ticker(ticker).dict()['payload']
        r = response_sample.copy()
        if response['total'] != 0:
            response = response['instruments'][0]
            data_price = client.get_market_orderbook(response['figi'], 0)
            response['last_price'] = data_price.dict()['payload']['last_price']
            r['payload'] = response
            r['total'] = len(r['payload'])

        return Response(r)


class MarketCurrenciesList(APIView):
    permission_classes = [AllowAny, ]
    
    def get(self, request):
        client = ti.SyncClient(SANDBOX_TOKEN, use_sandbox=True)
        register = client.register_sandbox_account(ti.SandboxRegisterRequest.tinkoff())
        data = client.get_market_currencies().dict()['payload']['instruments']
        r = response_sample.copy()
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

        return Response(r)


class MarketCurrenciesDetail(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, currency):
        client = ti.SyncClient(SANDBOX_TOKEN, use_sandbox=True)
        register = client.register_sandbox_account(ti.SandboxRegisterRequest.tinkoff())
        data = client.get_market_currencies().dict()['payload']['instruments']
        r = response_sample.copy()
        data_json = []
        for item in data:
            if item["ticker"][:3] == currency.upper():
                data_price = client.get_market_orderbook(item['figi'], 0)
                item['last_price'] = data_price.dict()['payload']['last_price']
                data_json = item

        r['payload'] = data_json
        r['total'] = len(r['payload'])

        return Response(r)


class QuartEarnings(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, ticker_name):
        tick = yf.Ticker(ticker_name)
        data = tick.quarterly_earnings
        r = response_sample.copy()
        data_json = []

        if data is not None:
            data_json.append(data.to_dict(orient='index'))
            r['payload'] = data_json
            r['total'] = len(r['payload'])

        return Response(r)


class Info(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, ticker_name):
        tick = yf.Ticker(ticker_name)
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
    permission_classes = [AllowAny, ]

    def get(self, request, ticker_name):
        tick = yf.Ticker(ticker_name)
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
    permission_classes = [AllowAny, ]

    def get(self, request, ticker_name):
        tick = yf.Ticker(ticker_name)
        data = tick.info
        r = response_sample.copy()

        if len(data) > 2:
            time = data['exDividendDate']
            data_json = {'next_div_day': time}
            r['payload'] = [data_json]
            r['total'] = len(r['payload'])

        return Response(r)


class NextEarns(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, ticker_name):
        tick = yf.Ticker(ticker_name)
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
    permission_classes = [AllowAny,]

    def get(self, request, ticker, days=10):
        data = services.get_insiders(ticker, days)
        return Response(services.pd_insiders(data))


class CheckPortfolioStocks(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        r = response_sample.copy()

        if 'sandbox_token' in data:
            try:
                client = ti.SyncClient(data['sandbox_token'], use_sandbox=True)
                accounts = client.get_accounts().payload.accounts
                broker_account_id = accounts[0].broker_account_id

                r['payload'] = client.get_portfolio(broker_account_id).payload.positions
                r['total'] = len(r['payload'])
            except UnexpectedError as e:
                r['code'] = int(str(e))
        else:
            r['code'] = 400

        return Response(r)


class CheckPortfolioCurrencies(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        r = response_sample.copy()

        if 'sandbox_token' in data:
            try:
                client = ti.SyncClient(data['sandbox_token'], use_sandbox=True)
                accounts = client.get_accounts().payload.accounts
                broker_account_id = accounts[0].broker_account_id

                r['payload'] = client.get_portfolio_currencies(broker_account_id).payload.currencies
                r['total'] = len(r['payload'])
            except UnexpectedError as e:
                r['code'] = int(str(e))
        else:
            r['code'] = 400

        return Response(r)


class StocksMarketOrder(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        r = response_sample.copy()

        if 'sandbox_token' in data:
            try:
                client = ti.SyncClient(data['sandbox_token'], use_sandbox=True)
                accounts = client.get_accounts().payload.accounts
                broker_account_id = accounts[0].broker_account_id
                info = client.get_market_search_by_ticker(data['ticker']).dict()['payload']
                if info['total'] != 0:
                    figi = info['instruments'][0]['figi'], 0
                    body = ti.MarketOrderRequest(
                        lots=data['lots'],
                        operation=data['operation']
                    )
                    try:
                        client.post_orders_market_order(figi, body, broker_account_id)
                        r['payload'] = client.get_portfolio(broker_account_id).payload.positions
                        r['total'] = len(r['payload'])
                    except UnexpectedError as e:
                        r['detail'] = eval(e.text)['payload']['code']
                else:
                    r['detail'] = 'invalid ticker'
            except UnexpectedError as e:
                r['code'] = int(str(e))
        else:
            r['code'] = 400

        return Response(r)


class CurrenciesMarketOrder(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        r = response_sample.copy()

        if 'sandbox_token' in data:
            try:
                client = ti.SyncClient(data['sandbox_token'], use_sandbox=True)
                accounts = client.get_accounts().payload.accounts
                broker_account_id = accounts[0].broker_account_id
                info = client.get_market_currencies().dict()['payload']['instruments']
                figi = None
                for item in info:
                    if item["ticker"][:3] == data['ticker'].upper():
                        figi = item['figi']

                    if figi is not None:
                        body = ti.MarketOrderRequest(
                            lots=data['lots'],
                            operation=data['operation']
                        )
                        try:
                            client.post_orders_market_order(figi, body, broker_account_id)
                            r['payload'] = client.get_portfolio(broker_account_id).payload.positions
                            r['total'] = len(r['payload'])
                        except UnexpectedError as e:
                            r['detail'] = eval(e.text)['payload']['code']
                    else:
                        r['detail'] = 'invalid ticker'
            except UnexpectedError as e:
                r['code'] = int(str(e))
        else:
            r['code'] = 400

        return Response(r)