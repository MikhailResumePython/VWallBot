import requests
import json
import re
import bot

#auth token Orlov
VK_ACCESS_TOKEN = '51ceef69886c8177ce720559f871b2d02ce0efd67895525656430907744b806bf78d783bbc329daba28ac'
VK_BASE_URL = 'https://api.vk.com/method/'


def get_posts(count='50', filters='post', start_from=None):
    url = ('{}newsfeed.get?filters={}&count={}&return_banned=0'
            '&access_token={}&v=5.80').format(VK_BASE_URL, filters, count, VK_ACCESS_TOKEN)
    if(start_from != None):
        url += '&start_from={}'.format(start_from)
    posts = requests.get(url)
    return posts.json()


def parse_posts(posts):
    parsed_posts = []
    for item in posts['response']['items']:
        if(item['is_pinned'] == 1):
            continue
        post_id = item['id']
        text = item['text']
        photos_url = []
        videos_url = []
        audio_url = None
        attached_link = None
        has_attached_album = False
        has_attached_photos_list = False
        for attachment in item['attachments']:
            if(attachment['type'] == 'photo'):
                for size in reversed(attachment['photo']['sizes']):
                    if(size['type'] == 'z' or size['type'] == 'y' 
                            or size['type'] == 'x' or size['type'] == 'm' or size['type'] == 's'):
                        photos_url.append(size['src'])
                        break
            elif(attachment['type'] == 'video'):
                videos_url.append(parse_video(attachment['video']))
            elif(attachment['type'] == 'link'):
                attached_link = attachment['link']['url']
            elif(attachment['type'] == 'doc'):
                pass
            elif(attachment['type'] == 'album'):
                attached_album = True
            elif(attachment['type'] == 'photos_list'):
                attached_photos_list = True

                        
def parse_video(video):
    '''Return video url from VK video object.

    Args:
    video -- VK video object
    '''
    url = VK_BASE_URL + 'video.get?owner_id=' + video['owner_id'] 
    url += '&videos=' + video['owner_id'] + '_' + video['id'] 
    url += 'count=1&extended=0&v=5.80&access_token=' + VK_ACCESS_TOKEN
    video_obj = requests.get(url)['response']['items'][0]
    video_url = video_obj['player']
    try:
        video_platform = video_obj['platform'].lower()
    except KeyError:
        video_url = 'https://vk.com/video' + video_obj['owner_id'] + '_' + video_obj['id'] 
        return video_url
    if(video_platform == 'youtube'):
        watch_v = re.search(r'\/(\w+)\?', video_url).group(1)
        video_url = 'https://www.youtube.com/watch?v=' + watch_v
    elif(video_platform == 'vimeo'):
        vimeo_video_id = re.search(r'\/(\w+)\?', video_url).group(1)
        video_url = 'https://vimeo.com/' + vimeo_video_id
    return video_url

