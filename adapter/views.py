from django.shortcuts import render
import tinvest as ti
from rest_framework.views import APIView
from rest_framework.response import Response
 
TOKEN = 't.Cz0mvF5Z-uPelMSg5eTTHTSe06y2E227cjLXqp09J4ZzjdFrsw7Mk1VG6fgiuE_iJWcPzYbNjpvB5LZUkIV92Q'
 
# регистрируем аккаунт
class MarketDetail(APIView):
    def get(self, request, ticker):
    # регистрируем аккаунт
        client = ti.SyncClient(TOKEN, use_sandbox=True)
        body = ti.SandboxRegisterRequest.tinkoff()
        register = client.register_sandbox_account(body)
        response = client.get_market_search_by_ticker(ticker)
        return Response(response)