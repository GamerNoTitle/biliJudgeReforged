import requests, json, os
from utils.biliAPI import base_info, qualification, apply
def convert_cookies_to_dict(cookie):
    cookie = dict([l.split("=", 1) for l in cookie.split("; ")])
    return cookie

class user:
    def __init__(self, SESSDATA, CSRF, UA):
        self.SESSDATA = SESSDATA
        self.CSRF = CSRF
        self.UA = UA

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

    def getQualification(self):
        headers = {
            'cookie': f'SESSDATA={self.SESSDATA}',
            'Host': 'api.bilibili.com',
            'User-Agent': self.UA
        }
        response = requests.get(qualification, headers=headers)
        data = json.loads(response.text)
        if data['code'] == -101: 
            self.login, self.blocked, self.cert, self.rule = False, None, None, None
        elif data['code'] == 0:
            self.login = True
            self.blocked = data['data']['blocked']
            self.cert = data['data']['cert']
            self.rule = data['data']['rule']

    def applyFor(self):
        self.getBaseInfo()
        self.getQualification()
        # print(self.login, self.blocked, self.cert, self.rule, self.login, self.allow_apply, self.apply_status, self.status)
        if self.login:
            if not self.blocked and self.cert and self.rule and self.allow_apply and self.apply_status != 5:
                # 登录，未被小黑屋，有实名，90天内无封禁，允许申请且此周期内没有申请过
                headers = {
                    'cookie': f'SESSDATA={self.SESSDATA}',
                    'Host': 'api.bilibili.com',
                    'User-Agent': self.UA
                }
                params = {'csrf': self.CSRF}
                response = requests.post(apply, params=params, headers=headers)
                data = json.loads(response.text)
                if data['code'] == 0:
                    print('[INFO] Welcome to JUDGEMENT!')
                elif data['code'] == -101:
                    print('[ERR] You are not logged in!')
                elif data['code'] == -111:
                    print('[ERR] Invalid CSRF token (bili_jct in your cookie)!')
                elif data['code'] == 25001:
                    print('[ERR] Your level is TOO low!')   # Previous version
                elif data['code'] == 25002:
                    print('[ERR] You are not surfing with your real name!')
                elif data['code'] == 25003:
                    print('[ERR] You have banned log in previous 90 days!')
                elif data['code'] == 25013:
                    print('[ERR] You can apply for qualification while you are already have it!')
                elif data['code'] == 25016:
                    print('[ERR] No more qualification today, please retry tomorrow!')
                if data['code'] != 0:
                    print(response.text)
                    os._exit(-1)
            else:
                print('[ERR] You are not qualified to JUDGEMENT!')
                os._exit(-1)
        else:
            print('[ERR] You are not logged in!')
            os._exit(-1)