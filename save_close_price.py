from utils import *
import pandas as pd
import yfinance as yf
from datetime import datetime
import time

def save_close_price():
    file_name = 'close_price.csv'
    df = pd.DataFrame(columns=TICKERS)
    prices = {}
    for ticker in TICKERS:
        close_price = int(yf.download(ticker, period='1d', progress=False).iloc[-1]['Close'] * 100) / 100
        prices[ticker] = close_price
        time.sleep(0.2)

    df = df.append([prices], ignore_index=True)
    df.to_csv(file_name, index=False)  # csv 파일에 저장
    print(f"close_price가 저장되었습니다. {datetime.now()}")


if __name__=='__main__':
    save_close_price()
