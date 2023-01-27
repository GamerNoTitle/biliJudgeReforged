import requests
import json
from utils.biliAPI import video_info


class video:
    def __init__(self, avid):
        self.avid = avid
        response = requests.get(f'{video_info}/?aid={self.avid}')
        self.data = json.loads(response.text)
        self.length = self.data['data']['duration']
        self.title = self.data['data']['title']
