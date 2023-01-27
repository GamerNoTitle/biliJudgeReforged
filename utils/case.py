import requests
import json
import time
import random
from logging import Logger
from math import ceil
from utils import biliAPI
from utils.video import video


class case:
    def __init__(self, cid: str, SESSDATA: str, UA: str, CSRF: str, logger: Logger):
        self.cid = cid
        self.SESSDATA = SESSDATA
        self.UA = UA
        self.CSRF = CSRF
        self.logger = logger
        self.headers = {
            'cookie': self.SESSDATA,
            'Host': 'api.bilibili.com',
            'User-Agent': self.UA
        }

    def getOpinion(self):
        response = requests.get(
            f'{biliAPI.opinion}/?case_id={self.cid}&pn=1&ps=20', headers=self.headers)
        self.logger.debug(response.text)
        data = json.loads(response.text)['data']
        count = data['total']
        opinion_list = data['list']
        if count == 0:
            pass
        elif count > 20:
            for page in range(2, ceil(count/20)):
                response = requests.get(
                    f'{biliAPI.opinion}/?case_id={self.cid}&pn={page}&ps=20', headers=self.headers)
                self.logger.debug(response.text)
                data = json.loads(response.text)['data']
                opinion_list += data['list']
        self.opinion_count = count
        self.opinion_list = opinion_list
        self.logger.debug(
            f'Opinion Count: {self.opinion_count} | Opinion List: {self.opinion_list}')
        self.exist_vote = []
        for opinion in self.opinion_list:
            self.exist_vote.append(opinion['vote'])
        if self.type in [1, 2]:
            self.vote_list = [(1, self.exist_vote.count(1)), (2, self.exist_vote.count(
                2)), (3, self.exist_vote.count(3)), (4, self.exist_vote.count(4))]
        else:
            self.vote_list = [(11, self.exist_vote.count(11)), (12, self.exist_vote.count(
                12)), (13, self.exist_vote.count(13)), (4, self.exist_vote.count(14))]
        self.vote_list.sort(key=lambda x: x[1], reverse=True)
        if [count for _, count in self.vote_list].count(self.vote_list[0][1]) >= 2:
            self.vote = self.default_vote
        else:
            self.vote = self.vote_list[0][0]
        self.logger.debug(f'Vote: {self.vote} | Vote List: {self.vote_list}')

    def getInfo(self):
        response = requests.get(
            f'{biliAPI.case_info}/?case_id={self.cid}', headers=self.headers)
        data = json.loads(response.text)
        self.type = data['data']['case_type']
        self.vote_items = [1, 2, 3, 4] if self.type in [
            1, 2] else [11, 12, 13, 14]
        self.default_vote = 4 if self.type in [1, 2] else 14
        self.avid = data['data']['avid']
        self.logger.debug(
            f'Case ID: {self.cid} | Case Avid: {self.avid} | Case Type: {self.type} | Case Item: {self.vote_items} | Case Default: {self.default_vote}')

    def goVote(self):
        self.getOpinion()
        self.getInfo()
        v = video(self.avid)
        self.logger.info(
            f'[INFO] Now trying to vote to case {self.cid} for video {v.title}({self.avid}). After calculating, the vote option has been set to {self.vote}')
        sleep = random.randint(10, v.length)
        self.logger.info(
            f'[INFO] Now sleep for {sleep} seconds to avoid banning.')
        params = {
            'case_id': self.cid,
            'vote': self.vote,
            'insiders': 0,
            'content': '',
            'anonymous': 1,
            'csrf': self.CSRF
        }
        try_times = 1
        while True:
            response = requests.post(
                f'{biliAPI.vote}', params=params, headers=self.headers)
            if response.status_code == 200:
                if json.loads(response.text)['code'] == 0:
                    self.logger.info(
                        f'[INFO] Successfully vote {self.vote} to case {self.cid}.')
                elif json.loads(response.text)['code'] == -101:
                    self.logger.error(
                        f'[ERR] You are not logged in when vote {self.vote} to case {self.cid}.')
                elif json.loads(response.text)['code'] == -111:
                    self.logger.error(
                        f'[ERR] Wrong CSRF when vote {self.vote} to case {self.cid}.')
                elif json.loads(response.text)['code'] == 25005:
                    self.logger.error(
                        f'[ERR] You are not judgement! Error when vote {self.vote} to case {self.cid}.')
                elif json.loads(response.text)['code'] == 25011:
                    self.logger.error(
                        f'[ERR] Wrong vote id {self.vote} to case {self.cid} with type {self.type}.')
                elif json.loads(response.text)['code'] == 25018:
                    self.logger.error(
                        f'[ERR] You can not do this when vote {self.vote} to case {self.cid}.')
                try_times = 1
                break
            else:
                self.logger.warn(f'[WARN] Cannot vote, retrying...')
                if try_times == 3:
                    self.logger.error(
                        f'[ERR] You have reached the limit of retrying times(3)! Giving up...')
                    break
