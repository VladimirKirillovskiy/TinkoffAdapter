from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from TinkoffAdapter.settings import SANDBOX_TOKEN
import tinvest as ti
import json
import adapter.services as services
 

class MarketDetail(APIView):
    permission_classes = [AllowAny,]
    
    def get(self, request, ticker):
        client = ti.SyncClient(SANDBOX_TOKEN, use_sandbox=True)
        register = client.register_sandbox_account(ti.SandboxRegisterRequest.tinkoff())
        response = client.get_market_search_by_ticker(ticker)
        return Response(json.loads(response.json()))


class Insiders(APIView):
    permission_classes = [AllowAny,]

    def get(self, request, ticker, days=10):
        data = services.get_insiders(ticker, days)
        return Response(services.pd_insiders(data))
