from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from TinkoffAdapter.settings import SANDBOX_TOKEN
import tinvest as ti
import json
 

class MarketDetail(APIView):
    permission_classes = [AllowAny,]
    
    def get(self, request, ticker):
        client = ti.SyncClient(SANDBOX_TOKEN, use_sandbox=True)
        register = client.register_sandbox_account(ti.SandboxRegisterRequest.tinkoff())
        response = client.get_market_search_by_ticker(ticker)
        return Response(json.loads(response.json()))


class Currencies(APIView):
    permission_classes = [AllowAny,]
    
    def get(self, request):
        client = ti.SyncClient(SANDBOX_TOKEN, use_sandbox=True)
        register = client.register_sandbox_account(ti.SandboxRegisterRequest.tinkoff())
        data = client.get_market_currencies().dict()['payload']['instruments']
        data_json = []
        for item in data:
            res = {}
            res['name'] = item['name']
            res['ticker'] = item['ticker']
            res['currency'] = item['currency']
            res['figi'] = item['figi']
            data_json.append(res)
        return Response(json.dumps(data_json, ensure_ascii=False))

