import requests
import json
from utils.biliAPI import video_info, cid_convert


class video:
    def __init__(self, avid, logger):
        self.avid = avid
        self.logger = logger
        response = requests.get(f'{video_info}?aid={self.avid}')
        self.logger.debug(response.text)
        self.data = json.loads(response.text)
        self.length = self.data['data']['duration']
        self.title = self.data['data']['title']
        response = requests.get(f'{cid_convert}?aid={self.avid}')
        self.logger.debug(response.text)
        self.cid_data = json.loads(response.text)
        self.cid = self.cid_data['data'][0]['cid']