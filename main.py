from flask import Flask, jsonify, request
import urllib3
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import datetime
import os
import csv
import yfinance as yf

urllib3.disable_warnings()
TICKERS = ['SOXL','BULZ','TQQQ','TECL','WEBL','UPRO','FNGU','HIBL','WANT',
           'TNA','NAIL','RETL','UDOW','LABU','PILL','CURE','MIDU','FAS','TPOR','DFEN','DUSL','DRN','DPST','BNKU','UTSL']

app = Flask(__name__)


def row2dict(row, get):
    '''

    :param row: pandas 마지막 한 줄
    :param get: 'cur_rsi' or 'close_price'
    :return: 사전 형태 리턴
    '''
    data = []
    for ticker in TICKERS:
        data.append({'ticker': ticker,
                     get: row[ticker]})
    return data


def get_cur_rsi(ticker):
    url = f'https://finviz.com/screener.ashx?v=171&ft=3&t={ticker}&o=rsi'
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'}
    html = requests.get(url=url, headers=headers)
    soup = bs(html.text, 'html.parser')
    rows = soup.find_all('a',class_="screener-link")
    rsi = float(rows[-6].text)
    return rsi


def get_cur_price(ticker):
    url = 'https://finance.yahoo.com/quote/' + ticker
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'}
    html = requests.get(url=url, headers=headers)
    soup = bs(html.text, 'html.parser')
    cur_price = soup.find_all('fin-streamer')[24].text
    return cur_price




@app.route('/getClosePrice')

def get_price():
    parameder_dict = request.args.to_dict()

    file_name = f'close_price.csv'
    now = datetime.datetime.now()
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    today_datetime = datetime.datetime.strptime(today, '%Y-%m-%d')

    if not os.path.exists(file_name):  # 파일이 없다면 파일 저장
        df = pd.DataFrame(columns=TICKERS)
        df.to_csv(file_name)

    df = pd.read_csv(file_name)  # 파일 읽기
    if len(df) == 0:
        save_time = today_datetime - datetime.timedelta(days=1)

    else:
        save_time = datetime.datetime.strptime(df.iloc[-1]['Day'], '%Y-%m-%d')

    if (now - today_datetime).seconds > 14700 and (today_datetime - save_time).days == 1:  # am 5시 이후 인 경우, 데이터 저장
        prices = {}
        for ticker in TICKERS:
            close_price = int(yf.download(ticker, start=today).iloc[-1]['Close'] * 100) / 100
            prices[ticker] = close_price
        prices['Day'] = today
        df = df.append(prices, ignore_index=True)
        df.to_csv(file_name)  # 파일 저장

    row = df.iloc[-1]

    if len(parameder_dict) == 0:
        data = row2dict(row, 'close_price')

    else:
        ticker = list(parameder_dict.values())[0]
        close_price = row[ticker]
        data = []
        data.append({'ticker':ticker, 'close_price':close_price})

    resp = jsonify(data)

    return resp







@app.route('/getRSI')
def get_rsi():
    now = datetime.datetime.now()
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    today_datetime = datetime.datetime.strptime(today, '%Y-%m-%d')
    file_name = 'RSI-data.csv'

    if not os.path.exists(file_name):  # 파일명이 없을 때
        df = pd.DataFrame(columns=TICKERS)
        df.to_csv(file_name, index=False)

    df = pd.read_csv(file_name)  # 파일 읽기

    if len(df) == 0:
        save_time = today_datetime - datetime.timedelta(days=1)

    else:
        save_time = datetime.datetime.strptime(df.iloc[-1]['Day'], '%Y-%m-%d')

    if (now - today_datetime).seconds > 36000 and (today_datetime - save_time).days == 1:  # am 10시 이후 인 경우 , 데이터 저장

        rsis = {}
        for ticker in TICKERS:
            rsi = get_cur_rsi(ticker)
            rsis[ticker] = rsi

        rsis['Day'] = today
        df = df.append([rsis])

        df.to_csv('RSI-data.csv', index=False)

    row = df.iloc[-1]
    data = row2dict(row, 'cur_rsi')
    resp = jsonify(data)

    return resp









if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True, port=9999)
