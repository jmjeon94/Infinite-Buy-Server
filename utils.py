from bs4 import BeautifulSoup as bs
import requests

TICKERS = ['SOXL','BULZ','TQQQ','TECL','WEBL','UPRO','FNGU','HIBL','WANT',
           'TNA','NAIL','RETL','UDOW','LABU','PILL','CURE','MIDU','FAS','TPOR','DFEN','DUSL','DRN','DPST','BNKU','UTSL']

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


def round_price(price, ndigits=2):
    return round(price, ndigits)

