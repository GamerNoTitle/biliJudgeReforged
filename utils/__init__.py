import os
from utils.action import convert_cookies_to_dict, user
from dotenv import load_dotenv, dotenv_values
import utils.const as const
from utils.logger import logger as log
load_dotenv()
loglevel = dotenv_values()['LOGLEVEL']
if dotenv_values()['SAVELOG'] == '1':
    logger = log(log_level = loglevel, log_file='info.log')
    logger.status = 1
else:
    logger = log(log_level = loglevel)
    logger.status = 0
SESSDATA, CSRF = dotenv_values()['SESSDATA'], dotenv_values()['CSRF']
if SESSDATA == '' or CSRF == '':
    logger.error('[ERROR] You must configure SESSDATA and CSRF to use this script!')
    os._exit(-1)
UA = dotenv_values()['UA']
if UA == '':
    UA = const.UA
    logger.warn(f'[WARN] It seems that you haven\'t configurate the UA, use fallback UA [{UA}] instead.')

my = user(SESSDATA, CSRF, UA, logger)
my.applyFor()