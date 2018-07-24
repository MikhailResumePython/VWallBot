from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
import bot
import vk
import tools


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
    tools.log_json(bot.send_media_group(166240669, [{'type': 'photo', 'media': 'https://pp.userapi.com/c846124/v846124612/a6b12/A3DZnLYUfGg.jpg'}, {'type': 'photo', 'media': 'https://pp.userapi.com/c846124/v846124612/a6b12/A3DZnLYUfGg.jpg'}]), 'test.log')
    #app.run(host='127.0.0.1', port=8080)

