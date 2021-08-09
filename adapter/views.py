from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from TinkoffAdapter.settings import SANDBOX_TOKEN
import tinvest as ti
import json
response_sample = {
    'payload': [],
    'total': 0,
}
class MarketDetail(APIView):
    permission_classes = [AllowAny,]
    def get(self, request, ticker):
        client = ti.SyncClient(SANDBOX_TOKEN, use_sandbox=True)
        register = client.register_sandbox_account(ti.SandboxRegisterRequest.tinkoff())
        response = client.get_market_search_by_ticker(ticker)
        return Response(json.loads(response.json()))



class MarketCurrenciesDetail(APIView):
    permission_classes = [AllowAny,]
    def get(self, request, currency):
        client = ti.SyncClient(SANDBOX_TOKEN, use_sandbox=True)
        register = client.register_sandbox_account(ti.SandboxRegisterRequest.tinkoff())
        data = client.get_market_currencies().dict()['payload']['instruments']
        r = response_sample.copy()
        data_json = []
        for item in data:
            if item["currency"] == currency:
                res = {
                  'currency': item['currency'],
                  'name': item['name'],
                  'ticker': item['ticker'],
                  'currency': item['currency'],
                  'min_price_increment': item['min_price_increment'],
                }
                data_json.append(res)
        r['payload'] = data_json
        r['total'] = len(r['payload'])
        return Response(r)