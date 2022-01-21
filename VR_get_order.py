import pandas as pd

RATIO_RISE = [1, 1.001, 1.005, 1.01, 1.015, 1.02, 1.025, 1.03, 1.035, 1.04, 1.045, 1.05, 1.055, 1.06, 1.065, 1.07,
              1.075, 1.08, 1.085, 1.09, 1.095, 1.1, 1.105, 1.11, 1.115]


def get_expect_value(n, post_expect_value):
    df_1 = pd.read_csv("VR_account.csv")
    pool = df_1.iloc[0]['pool']

    df_2 = pd.read_csv('close_price.csv')
    close_price = df_2.iloc[0]["TQQQ"]

    real_value = close_price * n

    if pool / post_expect_value <= 0.01:
        candidate = RATIO_RISE[0:2]

    else:
        number = int(pool / post_expect_value / 0.05) + 1
        candidate = RATIO_RISE[number:number + 2]

    if real_value >= post_expect_value:  # 평가금이 V보다 이상인경우
        ratio_rise = candidate[1]

    else:  # 평가금이 V보다 미만인 경우
        ratio_rise = candidate[0]

    expect_value = post_expect_value * ratio_rise + 250
    expect_value = round(expect_value, 2)

    return expect_value


def update_pool():
    df = pd.read_csv("VR_account.csv")
    df2 = df.copy()
    pool = df2['pool']
    pool += 250
    df2['pool'] = pool
    df2.to_csv("VR_account.csv", index=False)
    return df2.iloc[0]['pool']


def update_value(new_value):
    df = pd.read_csv("VR_account.csv")
    df['expect_value'] = new_value
    df.to_csv("VR_account.csv", index=False)


def make_order():
    file_name = "VR_account.csv"
    df = pd.read_csv(file_name)
    n = df.iloc[0]['n']
    post_expect_value = df.iloc[0]['expect_value']

    df_buy = pd.DataFrame(columns=['n', 'price', 'pool'])
    df_sell = pd.DataFrame(columns=['n', 'price', 'pool'])

    expect_value = get_expect_value(n=n, post_expect_value=post_expect_value)
    update_value(expect_value)

    max_value = expect_value * 1.25
    min_value = expect_value * 0.8

    pool = update_pool()
    qurter_pool = pool * 0.25

    buy_list = []
    sell_list = []

    pool_1 = pool
    pool_2 = pool

    n_1 = n
    n_2 = n

    while pool_1 > qurter_pool:  # 매수 주문서 작성
        price = round(min_value / n_1, 2)

        pool_1 -= price

        buy_list.append({'n': int(n_1 + 1), 'price': price, 'pool': round(pool_1, 2)})
        n_1 += 1

    i = 0
    while i < 12:  # 매도 주문서 작성
        price = round(max_value / n_2, 2)

        pool_2 += price

        sell_list.append({'n': int(n_2 - 1), 'price': price, 'pool': round(pool_2, 2)})
        n_2 -= 1
        i += 1

    df_buy = df_buy.append(buy_list, ignore_index=True)
    df_sell = df_sell.append(sell_list, ignore_index=True)

    df_buy.to_csv("VR_buy_list.csv", index=False)
    df_sell.to_csv("VR_sell_list.csv", index=False)


def reset_account():
    df = pd.DataFrame()
    df = df.append([{'n': 150, 'pool': 1232.88, 'expect_value': 12238.96}], ignore_index=True)
    df.to_csv("VR_account.csv", index=False)


if __name__ == '__main__':
    reset_account()
    make_order()
