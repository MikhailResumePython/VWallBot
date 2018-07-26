import requests
import json
import re
import bot

#auth token Orlov
VK_ACCESS_TOKEN = '51ceef69886c8177ce720559f871b2d02ce0efd67895525656430907744b806bf78d783bbc329daba28ac'
VK_BASE_URL = 'https://api.vk.com/method/'

class Post:
    '''VK post class.'''
    def __init__(self, group_name=None, ID=None, text=None, link=None, attached_link=None,
                    photos=None, videos=None, docs=None, has_audio=False, has_album=False,
                    has_photo_list=False, page=None):
        self.group_name = group_name
        self.ID = ID
        self.text = text
        self.link = link
        self.attached_link = attached_link
        self.photos = photos
        self.videos = videos
        self.docs = docs
        self.has_audio = has_audio
        self.has_album = has_album
        self.has_photo_list = has_photo_list
        self.page = page
        if photos == None:
            self.photos = []
        if videos == None:
            self.videos = []
        if docs == None:
            self.docs = []    


def get_posts(start_time = None):
    '''
    Return list of Post objects

    Args:
    start_time -- Identifier required to get the next page of results
    '''
    if start_time == '':
        start_time = None
    posts = newsfeed_get(start_time)
    bot.set_start_time(posts['response']['items'][0]['date'])
    return parse_posts(posts)


def newsfeed_get(start_time=None, count=1, filters='post'):
    '''
    Return data required to show newsfeed for the current user.

    Args:
    filters -- Listed comma-separated list of feed lists that you need to receive
    start_time -- Earliest timestamp (in Unix time) of a news item to return
    '''
    url = ('{}newsfeed.get?filters={}&return_banned=0'
            '&access_token={}&v=5.80').format(VK_BASE_URL, filters, VK_ACCESS_TOKEN)
    if start_time != None:
        url += '&start_time={}'.format(start_time)
    else:
        url += '&count={}'.format(count)
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
        post = Post()
        post.ID = item['post_id']
        post.group_name = get_group_name(abs(item['source_id']))
        post.text = item['text']
        post.link = 'https://vk.com/wall{}_{}'.format(item['source_id'], post.ID)
        for attachment in item['attachments']:
            if attachment['type'] == 'photo':
                for size in reversed(attachment['photo']['sizes']):
                    if (size['type'] == 'z' or size['type'] == 'y' or size['type'] == 'x'
                                            or size['type'] == 'm' or size['type'] == 's'):
                        post.photos.append(size['url'])
                        break
            elif attachment['type'] == 'video':
                post.videos.append(parse_video(attachment['video']))
            elif attachment['type'] == 'doc' and attachment['doc']['size'] < 10**7:
                post.docs.append(attachment['doc'])
            elif attachment['type'] == 'link':
                post.attached_link = attachment['link']['url']
            elif attachment['type'] == 'page':
                post.page = attachment['page']['view_url']
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
    video_obj = requests.get(url).json()['response']['items'][0]
    video_url = video_obj['player']
    try:
        video_platform = video_obj['platform'].lower()
    except KeyError:
        video_url = 'https://vk.com/video{}_{}'.format(video_obj['owner_id'], video_obj['id'])
        return video_url
    if video_platform == 'youtube':
        watch_v = re.search(r'\/([^\/]+)\?', video_url).group(1)
        video_url = 'https://www.youtube.com/watch?v=' + watch_v
    elif video_platform == 'vimeo':
        vimeo_video_id = re.search(r'\/([^\/]+)\?', video_url).group(1)
        video_url = 'https://vimeo.com/' + vimeo_video_id
    return video_url


def get_group_name(group_id):
    url = ('{}groups.getById?group_id={}'
            '&access_token={}&v=5.80').format(VK_BASE_URL, group_id,VK_ACCESS_TOKEN)
    group = requests.get(url)
    return group.json()['response'][0]['name']