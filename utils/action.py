import requests
import json
import os
from logging import Logger
from utils.biliAPI import base_info, qualification, apply, next_case


def convert_cookies_to_dict(cookie):
    cookie = dict([l.split("=", 1) for l in cookie.split("; ")])
    return cookie


class user:
    def __init__(self, SESSDATA, CSRF, UA, logger: Logger):
        self.SESSDATA = SESSDATA
        self.CSRF = CSRF
        self.UA = UA
        self.logger = logger
        self.headers = {
            'cookie': f'SESSDATA={self.SESSDATA}',
            'Host': 'api.bilibili.com',
            'User-Agent': self.UA
        }

    def getBaseInfo(self):
        headers = {
            'cookie': f'SESSDATA={self.SESSDATA}',
            'Host': 'api.bilibili.com',
            'User-Agent': self.UA
        }
        response = requests.get(base_info, headers=headers)
        data = json.loads(response.text)
        if data['code'] == -101:
            self.login = False
            self.allow_apply, self.apply_status, self.status = None, None, None
        elif data['code'] == 0:
            self.login = True
            self.allow_apply = data['data']['allow_apply']
            self.apply_status = data['data']['apply_status']
            self.status = data['data']['status']
        return response.text

    def getQualification(self):
        response = requests.get(qualification, headers=self.headers)
        data = json.loads(response.text)
        if data['code'] == -101:
            self.login, self.blocked, self.cert, self.rule = False, None, None, None
        elif data['code'] == 0:
            self.login = True
            self.blocked = data['data']['blocked']
            self.cert = data['data']['cert']
            self.rule = data['data']['rule']
        return response.text

    def applyFor(self):
        baseinfo = self.getBaseInfo()
        qualifi = self.getQualification()
        if self.logger.status:
            self.logger.debug(baseinfo)
            self.logger.debug(qualifi)
        if self.login:
            if self.status == 1:
                self.logger.info('[INFO] Welcome back, JUDGEMENT!')
            if self.apply_status == 5:
                pass
            elif not self.blocked and self.cert and self.rule and self.allow_apply and self.apply_status != 5:
                # 登录，未被小黑屋，有实名，90天内无封禁，允许申请且此周期内没有申请过
                params = {'csrf': self.CSRF}
                response = requests.post(
                    apply, params=params, headers=self.headers)
                data = json.loads(response.text)
                if self.logger.status:
                    self.logger.debug(response.text)
                if data['code'] == 0:
                    self.logger.debug(
                        '[INFO] Your application has been submitted. Please wait for ')
                elif data['code'] == -101:
                    self.logger.error('[ERR] You are not logged in!')
                elif data['code'] == -111:
                    self.logger.error(
                        '[ERR] Invalid CSRF token (bili_jct in your cookie)!')
                elif data['code'] == 25001:
                    # Previous version
                    self.logger.error('[ERR] Your level is TOO low!')
                elif data['code'] == 25002:
                    self.logger.error(
                        '[ERR] You are not surfing with your real name!')
                elif data['code'] == 25003:
                    self.logger.error(
                        '[ERR] You have banned log in previous 90 days!')
                elif data['code'] == 25013:
                    self.logger.error(
                        '[ERR] You can apply for qualification while you are already have done it. Please wait for pass!')
                elif data['code'] == 25016:
                    self.logger.error(
                        '[ERR] No more qualification today, please retry tomorrow!')
                if data['code'] != 0:
                    # print(response.text)
                    os._exit(-1)
            else:
                self.logger.error('[ERR] You are not qualified to JUDGEMENT!')
                os._exit(-1)
        else:
            self.logger.error('[ERR] You are not logged in!')
            os._exit(-1)

    def getCase(self):
        response = requests.get(next_case, headers=self.headers)
        data = json.loads(response.text)
        self.logger.debug(data)
        cid = None
        success = False
        if data['code'] == 0:
            cid = data['data']['case_id']
            success = True
        elif data['code'] == 25006:
            self.logger.error(
                '[ERR] Your JUDGEMENT qualification has been expired!')
        elif data['code'] == 25008:
            self.logger.error('[ERR] There\'s no case to be judged.')
        elif data['code'] == 25014:
            self.logger.error('[ERR] You have reach the limit of daily quote!')
        if not success:
            os._exit(-1)
        return cid
