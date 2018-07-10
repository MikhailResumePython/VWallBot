import requests
import json
import vk

BOT_TOKEN = '556191721:AAH11vENmvGlnHlDKnGiwWCnIIIdW5v-ntA'

BASE_URL = 'https://api.telegram.org/bot' + BOT_TOKEN + '/'

def handleUpdate(update):
    chat_id = update['message']['chat']['id']
    message_text = update['message']['text']
    if message_text == '/start':
        send_message(chat_id, '\xF0\x9F\x94\xAA')
    elif message_text == '/help':
        send_message(chat_id, 'help')

#TODO
# Create one handler to avoid duplication
def send_message(chat_id, text):
    url = BASE_URL + 'sendMessage'
    message = {'chat_id': chat_id, 'text': text}
    post = requests.post(url, json=message)
    return post.json()


def send_photo(chat_id, photo, caption=''):
    url = BASE_URL + 'sendPhoto'
    message = {'chat_id': chat_id, 'photo': photo, 'caption': caption}
    post = requests.post(url, json=message)
    return post.json()