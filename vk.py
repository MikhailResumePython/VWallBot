import requests
import json
import re

VK_ACCESS_TOKEN = 'd6b48fd0deea32e34f31285946d60dbb8269b60258d023b572290d9f33c3ea419476668ef5277a27c0ef9'
VK_BASE_URL = 'https://api.vk.com/method/'


def get_posts(domain, count):
    url = VK_BASE_URL + 'wall.get?domain=' + domain 
    url += '&count=' + count + '&filter=owner&v=5.80&access_token=' + VK_ACCESS_TOKEN
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
        pinned_audio = None
        for attachment in item['attachments']:
            if(attachment['type'] == 'photo'):
                for size in reversed(attachment['photo']['sizes']):
                    if(size['type'] == 'z' or size['type'] == 'y' 
                            or size['type'] == 'x' or size['type'] == 'm' or size['type'] == 's'):
                        photos_url.append(size['src'])
                        break
            elif(attachment['type'] == 'video'):
                videos_url.append(parse_video(attachment['video']))
            elif(attachment['type'] == 'audio'):
                pinned_audio = attachment['audio']['artist'] + ' - ' + attachment['audio']['title']
            elif(attachment['type'] == 'link'):
                pass
                        
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