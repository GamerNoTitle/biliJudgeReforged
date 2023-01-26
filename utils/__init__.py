import os
from utils.action import convert_cookies_to_dict, user
from dotenv import load_dotenv, dotenv_values
import utils.const as const
load_dotenv()
SESSDATA, CSRF = dotenv_values()['SESSDATA'], dotenv_values()['CSRF']
if SESSDATA == '' or CSRF == '':
    print('[ERROR] You must configure SESSDATA and CSRF to use this script!')
    os._exit(-1)
UA = dotenv_values()['UA']
if UA == '':
    UA = const.UA
    print(f'[WARN] It seems that you haven\'t configurate the UA, use fallback UA [{UA}] instead.')

my = user(SESSDATA, CSRF, UA)
my.applyFor()