import requests
import json
from vk import *
import io

BOT_TOKEN = '556191721:AAH11vENmvGlnHlDKnGiwWCnIIIdW5v-ntA'

BASE_URL = 'https://api.telegram.org/bot' + BOT_TOKEN + '/'


def log_json(data, filename):
    with open(filename, 'a') as log_file:
        json.dump(data, log_file, indent=2, ensure_ascii=False)
        log_file.write('\n\n')

def handleUpdate(update):
    chat_id = update['message']['chat']['id']
    try:
        message_text = update['message']['text']
    except KeyError:
        return 'KeyError: \'text\''
    returned_messages = []
    if message_text == '/start':
        rm = send_message(chat_id, u'🔪')
    elif message_text == '/help':
        rm = send_message(chat_id, 'no')
    elif message_text == 'pt':
        rm = send_photo(chat_id, 'https://pp.userapi.com//c626516//v626516637//57203//pCdItq4XreQ.jpg')
        returned_messages.append(rm)
        rm = send_message(chat_id, 'Мик Гордон подтвердил, что саундтрек DOOM Eternal будет иметь тот же стиль, что у перезапуска.\n\n\"Мы потратили очень много времени, чтобы определить звук DOOM, и мы не собираемся отказываться от него\"\n\nГотовьте свои ушки!', 'https://vk.com/dev/objects/post', 'VK link')
    elif message_text == 'ptg':
        rm = send_photo(chat_id, 'https://pp.userapi.com//c626516//v626516637//57203//pCdItq4XreQ.jpg', 'https://vk.com/dev/objects/post', 'VK link', 'Мик Гордон подтвердил, что саундтрек DOOM Eternal будет иметь тот же стиль, что у перезапуска.')
    elif message_text == 'sa':
        rm = send_audio(chat_id, 'https://cs9-17v4.vkuseraudio.net/p5/6914a6d0d82c38.mp3')
    returned_messages.append(rm)
    log_json(returned_messages, 'post_replies.log')


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


def send_photo(chat_id, photo, inline_url=None, inline_text=None, caption=''):
    url = BASE_URL + 'sendPhoto'
    if inline_url != None and inline_text != None:
        ikb = {'text': inline_text, 'url': inline_url}
        ikm = {'inline_keyboard': [[ikb]]}
        message = {'chat_id': chat_id, 'photo': photo, 'caption': caption, 'reply_markup': ikm}
    else:
        message = {'chat_id': chat_id, 'photo': photo, 'caption': caption}
    post = requests.post(url, json=message)
    return post.json()


def send_audio(chat_id, audio_url, performer='Unknown', title='Unknown'):
    url = '{}sendAudio?chat_id={}&performer={}&title={}'.format(BASE_URL, chat_id, performer, title)
    remote_file = requests.get(audio_url)
    file1 = io.BytesIO(remote_file.content)
    files = dict({'audio': file1})
    post = requests.post(url, files=files)
    return post.json()