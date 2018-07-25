import tools
import tg_methods as tg
import vk


def start_bot():
    TMP_chat_id = '166240669'
    posts = vk.get_posts()
    send_posts(TMP_chat_id, posts)


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


def send_posts(chat_id, posts):
    for post in posts:
        videos_count = len(post.videos)
        photos_count = len(post.photos)
        text = post.text
        text_is_fittable = True
        if post.attached_link != None:
            text += '\n' + post.attached_link
        if post.has_album != None:
            text += '\nVWallBot:[VK Album]'
        if post.has_album != None:
            text += '\nVWallBot:[VK Photo List]'
        if post.has_album != None:
            text += '\nVWallBot:[VK Audio]'
        if len(text) > 200:
            text_is_fittable = False

        if len(post.docs) == 1:
            if text_is_fittable == True:
                tg.send_document(chat_id, post.docs[0], text, post.link)
            else:
                tg.send_document(chat_id, post.docs[0], text)
                tg.send_message(chat_id, text, post.link)
        elif len(post.docs) > 1:
            for doc in post.docs:
                tg.send_document(chat_id, doc, text)
            tg.send_message(chat_id, text, post.link)

        if photos_count == 1 and videos_count == 0:
            if text_is_fittable == True:
                tg.send_photo(chat_id, post.photos[0], text, post.link)
            else:
                tg.send_photo(chat_id, post.photos[0])
                tg.send_message(chat_id, text, post.link)
        elif photos_count > 1 and videos_count == 0:
            tg.send_media_group(chat_id, convert_to_IM(post.photos, 'photo'))
            tg.send_message(chat_id, text, post.link)
        elif videos_count == 1 and photos_count == 0:
            if text_is_fittable == True:
                tg.send_video(chat_id, post.videos[0], text, post.link)
            else:
                tg.send_video(chat_id, post.videos[0])
                tg.send_message(chat_id, text, post.link)
        elif videos_count > 1 and photos_count == 0:
            tg.send_media_group(chat_id, convert_to_IM(post.videos, 'video'))
            tg.send_message(chat_id, text, post.link)
        elif videos_count >= 1 and photos_count >= 1:
            tg.send_media_group(chat_id, convert_to_IM(post.photos, 'photo'))
            tg.send_media_group(chat_id, convert_to_IM(post.videos, 'video'))
            tg.send_message(chat_id, text, post.link)
        else:
            tg.send_message(chat_id, text, post.link)
        
        



def convert_to_IM(array, IM_type):
    input_media =[]
    for media in array:
        input_media.append({'type': IM_type, 'media': media})
    return input_media