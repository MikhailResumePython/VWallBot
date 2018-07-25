import tools
import tg_methods as tg
import vk


def start_bot():
    pass


def handleUpdate(update):
    chat_id = update['message']['chat']['id']
    try:
        message_text = update['message']['text']
    except KeyError:
        return 'KeyError: \'text\''
    returned_messages = []
    rm = 'None'
    if message_text == '/start':
        rm = tg.send_message(chat_id, u'🔪')
    elif message_text == '/help':
        rm = tg.send_message(chat_id, 'no')
    returned_messages.append(rm)
    tools.log_json(returned_messages, 'post_replies.log')




