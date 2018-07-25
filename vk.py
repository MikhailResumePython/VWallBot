import requests
import json
import re
import bot

#auth token Orlov
VK_ACCESS_TOKEN = '51ceef69886c8177ce720559f871b2d02ce0efd67895525656430907744b806bf78d783bbc329daba28ac'
VK_BASE_URL = 'https://api.vk.com/method/'

class Post:
    '''VK post class.'''
    def __init__(self, post_id=None, text=None, link=None, photos=[], videos=[], 
                    docs=[], has_audio=False, has_album=False, has_photo_list=False):
        self.post_id = post_id
        self.text = text
        self.link = link
        self.photos = photos
        self.videos = videos
        self.docs = docs
        self.has_audio = has_audio
        self.has_album = has_album
        self.has_photo_list = has_photo_list


def get_posts(start_from = None):
    '''
    Return list of Post objects

    Args:
    start_from -- Identifier required to get the next page of results
    '''
    posts = newsfeed_get(start_from)
    return parse_posts(posts)


def newsfeed_get(start_from=None, filters='post'):
    '''
    Return data required to show newsfeed for the current user.

    Args:
    filters -- Listed comma-separated list of feed lists that you need to receive
    start_from -- Identifier required to get the next page of results
    '''
    url = ('{}newsfeed.get?filters={}&return_banned=0'
            '&access_token={}&v=5.80').format(VK_BASE_URL, filters, VK_ACCESS_TOKEN)
    if start_from != None:
        url += '&start_from={}'.format(start_from)
    else:
        url + '&count=10'
    posts = requests.get(url)
    return posts.json()


def parse_posts(posts):
    '''
    Return list of Post objects

    Args:
    posts -- VK API newsfeed.get method response
    '''
    parsed_posts = []
    for item in posts['response']['items']:
        if item['is_pinned'] == 1:
            continue
        post = Post()
        post.post_id = item['id']
        post.text = item['text']
        for attachment in item['attachments']:
            if attachment['type'] == 'photo':
                for size in reversed(attachment['photo']['sizes']):
                    if (size['type'] == 'z' or size['type'] == 'y' or size['type'] == 'x'
                                            or size['type'] == 'm' or size['type'] == 's'):
                        post.photos.append(size['src'])
                        break
            elif attachment['type'] == 'video':
                post.videos.append(parse_video(attachment['video']))
            elif attachment['type'] == 'doc' and attachment['doc']['size'] < 10**7:
                post.docs.append(attachment['doc'])
            elif attachment['type'] == 'link':
                post.link = attachment['link']['url']
            elif attachment['type'] == 'audio':
                post.has_audio = True
            elif attachment['type'] == 'album':
                post.has_album = True
            elif attachment['type'] == 'photos_list':
                post.has_photos_list = True   
        parsed_posts.append(post)
    return parsed_posts

                        
def parse_video(video):
    '''
    Return video url from VK video object.

    Args:
    video -- VK video object
    '''
    url = ('{}video.get?owner_id={}&videos={}_{}&count=1&extended=0&v=5.80'
            '&access_token={}').format(VK_BASE_URL, video['owner_id'], 
                                        video['owner_id'], video['id'], VK_ACCESS_TOKEN)
    video_obj = requests.get(url)['response']['items'][0]
    video_url = video_obj['player']
    try:
        video_platform = video_obj['platform'].lower()
    except KeyError:
        video_url = 'https://vk.com/video' + video_obj['owner_id'] + '_' + video_obj['id'] 
        return video_url
    if video_platform == 'youtube':
        watch_v = re.search(r'\/(\w+)\?', video_url).group(1)
        video_url = 'https://www.youtube.com/watch?v=' + watch_v
    elif video_platform == 'vimeo':
        vimeo_video_id = re.search(r'\/(\w+)\?', video_url).group(1)
        video_url = 'https://vimeo.com/' + vimeo_video_id
    return video_url

