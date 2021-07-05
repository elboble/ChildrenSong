import os
import time
import uuid

import requests

from setting import MONGO_DB, AUDIO_PATH, COVER_PATH

sid_list = [7713678, 7713760, 7713763, 7713768, 7713678, 7713675]
audioInfo_list = []


def caiji(aid):
    pageUrl = f"https://m.ximalaya.com/mobile/v1/track/share/content?trackId={aid}&tpName=weixin&device=h5"
    ret_dict = requests.request('get', pageUrl).json()

    title = ret_dict['title']
    nickname = ret_dict['nickname']

    audioUrl = ret_dict['audioUrl']
    picUrl = ret_dict['picUrl']
    song = requests.request('get', audioUrl)
    cover = requests.request('get', picUrl)

    # print(song.content)

    filename = uuid.uuid4()
    audio_path = os.path.join(AUDIO_PATH, f'{filename}.mp3')
    cover_path = os.path.join(COVER_PATH, f'{filename}.jpg')

    with open(audio_path, 'wb') as fp:
        fp.write(song.content)

    with open(cover_path, 'wb') as cp:
        cp.write(cover.content)

    audioInfo = {
        'title': title,
        'nickname': nickname,
        'audio_path': f'{filename}.mp3',
        'cover_path': f'{filename}.jpg'
    }

    return audioInfo


for sid in sid_list:
    print(f"caiji {sid}...", end='')
    audioInfo_list.append(caiji(sid))
    print('OK!')
    time.sleep(1)

MONGO_DB.erge.insert_many(audioInfo_list)
