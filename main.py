from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
import bot
import vk


app = Flask(__name__)


@app.route('/')
def index():
    return 'Get out of my room'


@app.route('/webhook', methods=['POST', 'GET'])
def index_webhook():
    if request.method == 'POST':
        update = request.get_json()
        bot.log_json_update(update)
        bot.handleUpdate(update)
        return jsonify(update)
    return 'hi'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)