from flask import Flask, jsonify, request

import pandas as pd
import datetime
import os
import yfinance as yf
from utils import *

app = Flask(__name__)

@app.route('/')
def root():
    return 'hello world'

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


@app.route('/getPriceHistory')
def get_price_history():
    ticker_name = request.args.get('ticker_name')
    start_date = request.args.get('start_date')

    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = start_date + datetime.timedelta(days=100)

    df = yf.download(ticker_name, start=start_date, end=end_date, progress=False)

    data = {'date': [date.strftime('%Y-%m-%d') for date in df.index],
            'close': df['Close'].apply(round_price).tolist(),
            'high': df['High'].apply(round_price).tolist(),
            # 'low': df['Low'].tolist()
            }

    resp = jsonify(data)
    return resp


if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

