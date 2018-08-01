import requests
import json
import io
from VWB import vk, tools



BOT_TOKEN = '556191721:AAH11vENmvGlnHlDKnGiwWCnIIIdW5v-ntA'

BASE_URL = 'https://api.telegram.org/bot' + BOT_TOKEN + '/'



def make_request(method, message):
    '''
    Make a query to the Telegram Bot API.

    Args:
    method -- Method name
    message -- json to send
    '''
    url = BASE_URL + method
    post = requests.post(url, json=message)
    post = post.json()
    tools.log_json(post, 'request_replies.log')
    return post


def append_inline_link(message, inline_url, inline_text):
    '''
    Append inline link to the message.

    Args:
    message -- The message
    inline_url -- URL link
    inline_text -- Text in URL button
    '''
    ikb = {'text': inline_text, 'url': inline_url}
    ikm = {'inline_keyboard': [[ikb]]}
    message['reply_markup'] = ikm
    return message



'''Down below are Bot API methods'''


def send_message(chat_id, text, inline_url=None, inline_text='VK link'):
    message = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    if inline_url != None and inline_text != None:
        message = append_inline_link(message, inline_url, inline_text)
    return make_request('sendMessage', message)


def send_photo(chat_id, photo, caption='', inline_url=None, inline_text='VK link'):
    message = {'chat_id': chat_id, 'caption': caption, 'photo': photo, 'parse_mode': 'HTML'}
    if inline_url != None and inline_text != None:
        message = append_inline_link(message, inline_url, inline_text)
    return make_request('sendPhoto', message)


def send_video(chat_id, video, caption='', inline_url=None, inline_text='VK link'):
    message = {'chat_id': chat_id, 'video': video, 'caption': caption, 'parse_mode': 'HTML'}
    if inline_url != None and inline_text != None:
        message = append_inline_link(message, inline_url, inline_text)
    return make_request('sendVideo', message)


def send_media_group(chat_id, media):
    message = {'chat_id': chat_id, 'media': media}
    return make_request('sendMediaGroup', message)


def send_document(chat_id, document, caption='', inline_url=None, inline_text='VK link'):
    message = {'chat_id': chat_id, 'document': document, 'caption': caption, 'parse_mode': 'markdown'}
    if inline_url != None and inline_text != None:
        message = append_inline_link(message, inline_url, inline_text)
    return make_request('sendDocument', message)


def send_audio(chat_id, audio_url, performer='Unknown', title='Unknown'):
    url = '{}sendAudio?chat_id={}&performer={}&title={}'.format(BASE_URL, chat_id, performer, title)
    remote_file = requests.get(audio_url)
    file1 = io.BytesIO(remote_file.content)
    files = dict({'audio': file1})
    post = requests.post(url, files=files)
    return post.json()