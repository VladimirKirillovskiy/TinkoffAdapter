from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from TinkoffAdapter.settings import SANDBOX_TOKEN
import tinvest as ti
import yfinance as yf
import adapter.services as services


response_sample = {
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

        return Response(response)


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
            if item["currency"] == currency.upper():
                data_json.append(item)
        
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
