import urllib.parse

import pymongo

import os


PROJECT_PATH = os.path.abspath('./')
AUDIO_PATH = 'audio'
COVER_PATH = 'cover'
CHATS_PATH = 'chats'
CHATS_SYS_PATH = 'sys'
CHATS_COMMAND_PATH = 'command'
QR_PATH = 'QRcode'
QR_URL = 'https://127.0.0.1:8900/qrcode?text=%s'
SERV = 'https://127.0.0.1:8900'
CERT_PATH = 'cert'

PEM = os.path.join(CERT_PATH, 'secret.pem')
KEY = os.path.join(CERT_PATH, 'secret.key')

# client = pymongo.MongoClient(host='xwhone23.f3322.org', port=27017,)
username = urllib.parse.quote_plus('mydbsloth')
password = urllib.parse.quote_plus('leeyang1')
client = pymongo.MongoClient('mongodb://%s:%s@iscm.f3322.org' % (username, password), authSource='mydb', port=57027)
MONGO_DB = client['mydb']

from redis import Redis
REDIS_DB = Redis(host="127.0.0.1",port=6379,db=10)


RET = {
    "code": 0,
    "msg": "",
    "data": {}
}

""" 你的 APPID AK SK """
APP_ID = '23975198'
API_KEY = 'slgUjxzhAnug6wOyDF2Ob8z7'
SECRET_KEY = '03KMokHiL2H3Bfz3hjVlcScFtGEbag77'
VOICE = {
        'vol':5,
        'spd':5,
        'pit':5,
        'per':1,
    }

ERROR_MSG = 'error.mp3'

QINGYUNKE_URL = 'http://api.qingyunke.com/api.php?'
QINGYUNKE_KEY = 'free'
QINGYUNKE_APPID = '0'

QINGYUNKE_PAYLOAD = {'key':QINGYUNKE_KEY,
                     'appid': QINGYUNKE_APPID,
                     'msg': '你好'}





