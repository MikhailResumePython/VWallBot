from flask import Flask, request, jsonify
import requests
import json
from VWB import bot, tools, tg_methods as tg
import time


app = Flask(__name__)


@app.route('/')
def index():
    return 'Get out of my room'


@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        update = request.get_json()
        tools.log_json(update, 'updates.log')
        bot.handleUpdate(update)
        return jsonify(update)
    return 'hi'


@app.route('/auth', methods=['GET'])
def auth():
    #auth
    return 'Yay'


if __name__ == '__main__':
    bot.start_bot()
    #app.run(host='127.0.0.1', port=8080)


