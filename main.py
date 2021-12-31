from flask import Flask, jsonify
import random
app = Flask(__name__)

@app.route('/getPrice')
def get_price():
    data = jsonify([
        {'ticker':'TQQQ',
         'cur_price':random.randint(60, 80),},
        {'ticker': 'SOXL',
         'cur_price': random.randint(20, 50),},
        ],
    )
    return data

@app.route('/getRSI')
def get_rsi():
    data = jsonify([
        {'ticker':'TQQQ',
         'cur_rsi': random.randint(60, 80),},
        {'ticker': 'SOXL',
         'cur_rsi': random.randint(40, 50),},
        ],
    )
    return data


if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True)
