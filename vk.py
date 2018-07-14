import requests
import json

VK_ACCESS_TOKEN = '976dea4d0c914b20a8b7770acaec287f4d93b5a4223bc743fd97894ebf159e543348bedb9d2748173bb2e'

VK_WALL_GET_DOMAIN_URL = 'https://api.vk.com/method/wall.get?domain='
VK_WALL_GET_PARAMS = '&count=10&filter=owner&access_token=' + VK_ACCESS_TOKEN + '&v=5.80'
