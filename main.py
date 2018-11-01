import os
from flask import Flask, request, jsonify
import requests
import json



from VWB import bot, tools, tg_methods as tg
from VWB import tools


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

@app.route('/start', methods=['POST', 'GET']) # :)
def start():
    bot.start_bot()
    return 'Yay'


if __name__ == '__main__':
    tools.init_tokens('VWB/tokens.txt')
    os.mkdir(logs)
    try:
        bot.start_bot()
    except Exception as e:
        tools.log_err(e, 'errors.log')
    #app.run(host='127.0.0.1', port=8080)


