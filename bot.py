from flask import Flask, request
import requests
from flask import jsonify
import re
from flask_sslify import SSLify

token = '979461001:AAFw8ckQD3N1CTN2EoBlu86bCahq28cGMVc'

app = Flask(__name__)
sslify = SSLify(app)

URL = f'https://api.telegram.org/bot{token}/'


def send_message(chat_id, text):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


def parse_text(text):
    pattern = r'/\w+'
    coin = re.search(pattern, text).group()
    return coin[1:]


def get_price(coin):
    url = f'https://yobit.net/api/3/ticker/{coin}_usd'
    r = requests.get(url).json()
    price = r[f'{coin}_usd']['last']
    return price


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        pattern = r'/\w+'

        if re.search(pattern, message):
            price = get_price(parse_text(message))
            send_message(chat_id, text=price)

        return jsonify(r)
    return '<h1>Greetings!</h1>'


if __name__ == '__main__':
    app.run()
