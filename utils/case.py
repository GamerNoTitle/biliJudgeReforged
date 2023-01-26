import requests, json
from math import ceil
from utils import biliAPI 
class case:
    def __init__(self, cid):
        self.cid = cid
        global cookie, UA
        headers={
            'cookie': cookie,
            'Host': 'api.bilibili.com',
            'User-Agent': UA
        }
        response = requests.get(f'{biliAPI.opinion}/?case_id={self.cid}&pn=1&ps=20', headers=headers)
        data = json.loads(response.text)['data']
        count = data['total']
        opinion_list = data['list']
        if count == 0:
            pass
        elif count > 20:
            for page in range(2, ceil(count/20)):
                response = requests.get(f'{biliAPI.opinion}/?case_id={self.cid}&pn={page}&ps=20', headers=headers)
                data = json.loads(response.text)['data']
                opinion_list += data['list']
        self.opinion_count = count
        self.opinion_list = opinion_list


    def vote(self): pass