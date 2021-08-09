from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from TinkoffAdapter.settings import SANDBOX_TOKEN
import tinvest as ti
import adapter.services as services
 

response_sample = {
    'payload': [],
    'total': 0,
}


class MarketDetail(APIView):
    permission_classes = [AllowAny,]
    
    def get(self, request, ticker):
        client = ti.SyncClient(SANDBOX_TOKEN, use_sandbox=True)
        register = client.register_sandbox_account(ti.SandboxRegisterRequest.tinkoff())
        response = client.get_market_search_by_ticker(ticker).dict()['payload']
        r = response_sample.copy()
        r['payload'] = response['instruments']
        r['total'] = int(response['total'])
        return Response(r)


class MarketAll(APIView):
    permission_classes = [AllowAny,]

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


class Insiders(APIView):
    permission_classes = [AllowAny,]

    def get(self, request, ticker, days=10):
        data = services.get_insiders(ticker, days)
        return Response(services.pd_insiders(data))


class InsidersCodes(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, code='ALL'):
        r = response_sample.copy()
        r['payload'] = services.get_codes(code)
        r['total'] = len(r['payload'])
        return Response(r)
