import requests
from datetime import date, timedelta
from time import sleep
import pandas as pd
from TinkoffAdapter.settings import FINNHUB_TOKEN


def get_insiders(company_name: str, days: int) -> dict:
    url = 'https://finnhub.io/api/v1/stock/insider-transactions'

    to_ = str(date.today() + timedelta(days=1))
    from_ = str(date.today() - timedelta(days=days - 1))

    params = {
        'symbol': company_name,
        'to': to_,
        'token': FINNHUB_TOKEN
    }

    data = []
    i = 0
    response = {
        'payload': [],
        'total': 0
    }

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


def get_codes(code) -> dict:

    codes = {
        'A': 'Grant, award, or other acquisition of securities from the company',
        'C': 'Conversion of derivative security',
        'D': 'Sale or transfer of securities back to the company',
        'E': 'Expiration of short derivative position',
        'F': 'Payment of exercise price or tax liability using portion of securities received from the company',
        'G': 'Gift of securities by or to the insider',
        'H': 'Expiration (or cancellation) of long derivative position with value received',
        'I': 'Discretionary transaction in accordance resulting in acquisition or disposition of issuer securities',
        'J': 'Other acquisition or disposition (describe transaction)',
        'K': 'Transaction in equity swap or instrument with similar characteristics',
        'M': 'Exercise or conversion of derivative security received from the company',
        'O': 'Exercise of out-of-the-money derivative security',
        'P': 'Purchase of securities on an exchange or from another person ',
        'S': 'Sale of securities on an exchange or to another person',
        'U': 'Disposition pursuant to a tender of shares in a change of control transaction',
        'V': 'A transaction voluntarily reported on Form 4',
        'X': 'Exercise of in-the-money or at-the-money derivative security'
    }

    sources = [
        'https://www.sec.gov/files/forms-3-4-5.pdf',
        'https://www.sec.gov/about/forms/form4data.pdf'
    ]

    code = code.upper()

    if code == 'ALL':
        return [codes]
    elif code == 'SOURCES':
        return sources
    elif code in codes:
        return [codes[code]]
    else:
        return []
