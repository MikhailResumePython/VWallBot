from flask import Flask
from flask import request
from flask import jsonify
import requests
import json


BASE_URL = 'https://api.telegram.org/bot556191721:AAH11vENmvGlnHlDKnGiwWCnIIIdW5v-ntA/'


app = Flask(__name__)


@app.route('/')
def index():
    return 'Get out of my room'


@app.route('/webhook', methods=['POST'])
def index_webhook():
    if request.method == 'POST':
        update = request.get_json()
        handleUpdate(update)
        return jsonify(update)
    return 'hi'


def send_message(chat_id, text):
    url = BASE_URL + 'sendMessage'
    message = {'chat_id': chat_id, 'text': text}
    sent_message = requests.post(url, json=message)
    return sent_message.json()


def handleUpdate(update):
    chat_id = update['message']['chat']['id']
    message_text = update['message']['text']
    
    if message_text == '/start':
        send_message(chat_id, '\xF0\x9F\x94\xAA')
    elif message_text == '/help':
        send_message(chat_id, '')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)