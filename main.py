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
def get_close_price():
    file_name = 'dataset/close_price.csv'

    df = pd.read_csv(file_name)
    row = df.iloc[-1]
    data = row2dict(row, 'close_price')
    resp = jsonify(data)

    return resp


@app.route('/getRSI')
def get_rsi():

    file_name = 'dataset/RSI_data.csv'

    df = pd.read_csv(file_name)
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

@app.route('/getFamousSaying')
def get_famous_saying():
    file_name = 'dataset/famous_saying.csv'
    df = pd.read_csv(file_name)
    row = df.iloc[0][0]
    return row





if __name__=='__main__':
    app.run(host='0.0.0.0', debug=False, port=9999)

