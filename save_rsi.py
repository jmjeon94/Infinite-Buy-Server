from utils import *
import pandas as pd

def save_rsi():
    file_name = 'RSI_data.csv'
    df = pd.DataFrame(columns=TICKERS)
    rsis = {}
    for ticker in TICKERS:
        rsi = get_cur_rsi(ticker)
        rsis[ticker] = rsi

    df = df.append([rsis], ignore_index=True)
    df.to_csv(file_name, index=False)  # csv 파일에 저장
    print("rsi 값이 저장되었습니다.")

if __name__=='__main__':
    save_rsi()
    