import requests
from datetime import datetime, date, timedelta
from time import sleep
import pandas as pd
from TinkoffAdapter.settings import FINNHUB_TOKEN


def get_insiders(response: dict, company_name: str, days: int) -> dict:
    url = 'https://finnhub.io/api/v1/stock/insider-transactions'

    to_ = str(date.today() + timedelta(days=1))
    from_ = str(date.today() - timedelta(days=days - 1))

    params = {
        'symbol': company_name,
        'from': from_,
        'to': to_,
        'token': FINNHUB_TOKEN,
    }

    data = []
    i = 0

    while True:
        r = requests.get(url, params=params)

        if r.status_code == 429:
            sleep(1)
            continue

        r = r.json()['data']

        if len(r) == 0:
            break

        if r[-1]['transactionDate'] < from_:
            for i in range(len(r) - 1, -1, -1):
                if r[i]['transactionDate'] >= from_:
                    break
            else:
                return response

            cut_r = r[:i + 1]
            data.extend(cut_r)
            break

        last_date = r[-1]['transactionDate']

        for i in range(len(r) - 1, -1, -1):
            if r[i]['transactionDate'] != last_date:
                break

        if i == 0:
            cut_r = r
        else:
            cut_r = r[:i + 1]

        data.extend(cut_r)
        params['to'] = r[i]['transactionDate']

    response['payload'] = data
    response['total'] = len(data)

    return response


def pd_insiders(origin_data: dict) -> dict:

    if 'total' in origin_data and origin_data['total'] <= 0:
        return origin_data

    data = pd.DataFrame(origin_data['payload'])

    grouped_data = data.groupby(['name', 'filingDate', 'transactionDate'])

    result = []
    columns = ['name', 'share', 'changePlus', 'transPricePlus', 'changeMinus', 'transPriceMinus', 'percentChange',
               'transactionDate', 'filingDate']

    for name, group in grouped_data:
        shareFinal = group['share'].iloc[0]
        shareStart = group['share'].iloc[-1] - group['change'].iloc[-1]  # количество акций до первой операции

        changePlus, changeMinus = 0, 0
        transPricePlus, transPriceMinus = 0, 0
        countPlus, countMinus = 0, 0

        for index, row in group.iterrows():
            if row['change'] > 0:
                changePlus += row['change']
                transPricePlus += row['transactionPrice']
                countPlus += 1
            else:
                changeMinus += row['change']
                transPriceMinus += row['transactionPrice']
                countMinus += 1

        if countPlus != 0:
            transPricePlus /= countPlus

        if countMinus != 0:
            transPriceMinus /= countMinus

        if shareStart != 0:
            percentChange = (shareFinal - shareStart) / shareStart * 100
        else:
            percentChange = 0

        temp = [name[0], shareFinal, changePlus, transPricePlus, changeMinus, transPriceMinus,
                percentChange, name[2], name[1]]

        result.append(temp)

    result_data = pd.DataFrame(result, columns = columns).round(2).sort_values(by = ['transactionDate'], ascending = False)

    origin_data['payload'] = result_data.to_dict(orient='records')
    origin_data['total'] = len(origin_data['payload'])
    return origin_data


def get_news_sentiment(r: dict, ticker: str):
    url = 'https://finnhub.io/api/v1/news-sentiment'
    params = {
        'symbol': ticker,
        'token': FINNHUB_TOKEN,
    }

    while True:
        response = requests.get(url, params=params)

        if response.status_code == 429:
            sleep(1)
            continue
        else:
            response = response.json()
            if len(response.keys()) == 1:  # если нет информации по тикеру
                r['code'] = 204
                r['detail'] = 'no data for ticker. accepted only US companies'
            else:
                r['payload'] = [response]
                r['total'] = 1
            break

    return r


def get_news_company(r: dict, ticker: str, days: int) -> dict:
    url = 'https://finnhub.io/api/v1/company-news'
    params = {
        'symbol': ticker,
        'from': str(date.today() - timedelta(days=days)),
        'to': str(date.today() + timedelta(days=1)),
        'token': FINNHUB_TOKEN,
    }

    while True:
        response = requests.get(url, params=params)

        if response.status_code == 429:
            sleep(1)
            continue
        else:
            response = response.json()
            if len(response) == 0:  # если нет информации по тикеру
                r['code'] = 204
                r['detail'] = 'no data for ticker. accepted only NA companies'
            else:
                data = []
                for item in response:
                    if item['summary'] == '':  # фильтр пустых новостей
                        continue

                    kit = {
                        'source': item['source'],
                        'category': item['category'],
                        'related': item['related'],
                        'utc': datetime.utcfromtimestamp(item['datetime']),
                        'summary': item['summary'],
                        'image': item['image'],
                        'url': item['url'],
                    }
                    data.append(kit)

                r['payload'] = sorted(data, key=lambda item: item['utc'], reverse=True)
                r['total'] = len(data)
            break

    return r
