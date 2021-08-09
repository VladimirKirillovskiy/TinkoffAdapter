from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from TinkoffAdapter.settings import SANDBOX_TOKEN
import tinvest as ti
import json
import yfinance as yf

response_sample = {
    'payload': [],
    'total': 0,
}


class MarketDetail(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, ticker):
        client = ti.SyncClient(SANDBOX_TOKEN, use_sandbox=True)
        register = client.register_sandbox_account(ti.SandboxRegisterRequest.tinkoff())
        response = client.get_market_search_by_ticker(ticker)
        return Response(json.loads(response.json()))


class MarketCurrencies(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        client = ti.SyncClient(SANDBOX_TOKEN, use_sandbox=True)
        register = client.register_sandbox_account(ti.SandboxRegisterRequest.tinkoff())
        data = client.get_market_currencies().dict()['payload']['instruments']
        r = response_sample.copy()
        data_json = []
        for item in data:
            res = {}
            res['name'] = item['name']
            res['ticker'] = item['ticker']
            res['currency'] = item['currency']
            data_json.append(res)
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
        data_json = []
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
            data_r = []
            data_r.append(data_json)
            r['payload'] = data_r
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
                res = {}
                res['data'] = item.value // 10 ** 9
                res['value'] = data[item]
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
        data_json = []
        if len(data) > 2:
            time = data['exDividendDate']
            data_json = {'next_div_day': time}
            data_r = []
            data_r.append(data_json)
            r['payload'] = data_r
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
            data_json = {}
            data_json['Date'] = data.loc[data.index.values[0], col].value // 10 ** 9
            data_json['EPS'] = data.loc[data.index.values[1], col]
            data_json['Revenue'] = data.loc[data.index.values[4], col]
            data_r = []
            data_r.append(data_json)
            r['payload'] = data_r
            r['total'] = len(r['payload'])
        return Response(r)
