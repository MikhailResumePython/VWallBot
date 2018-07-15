import requests
import json
import vk

BOT_TOKEN = '556191721:AAH11vENmvGlnHlDKnGiwWCnIIIdW5v-ntA'

BASE_URL = 'https://api.telegram.org/bot' + BOT_TOKEN + '/'


def log_json_update(update):
    with open('updates.log', 'a') as log_file:
        json.dump(update, log_file, indent=2, ensure_ascii=False)
        log_file.write('\n\n')

def handleUpdate(update):
    chat_id = update['message']['chat']['id']
    try:
        message_text = update['message']['text']
    except KeyError:
        return 'KeyError: \'text\''
    if message_text == '/start':
        send_message(chat_id, u'🔪')
    elif message_text == '/help':
        send_message(chat_id, 'no')

#TODO
# Create one handler to avoid duplication

def send_message(chat_id, text, inline_url=None, inline_text=None):
    url = BASE_URL + 'sendMessage'
    if inline_url != None and inline_text != None:
        ikb = {'text': inline_text, 'url': inline_url}
        ikm = {'inline_keyboard': [[ikb]]}
        message = {'chat_id': chat_id, 'text': text, 'reply_markup': ikm}
    else:
        message = {'chat_id': chat_id, 'text': text}
    post = requests.post(url, json=message)
    return post.json()


def send_photo(chat_id, photo, caption='', inline_url=None, inline_text=None):
    url = BASE_URL + 'sendPhoto'
    if inline_url != None and inline_text != None:
        ikb = {'text': inline_text, 'url': inline_url}
        ikm = {'inline_keyboard': [[ikb]]}
        message = {'chat_id': chat_id, 'photo': photo, 'caption': caption, 'reply_markup': ikm}
    else:
        message = {'chat_id': chat_id, 'photo': photo, 'caption': caption}
    post = requests.post(url, json=message)
    return post.json()