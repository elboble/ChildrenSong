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



def caiji_santi(directory,subclass):
    import os
    g = os.walk(directory)

    for path, dir_list, file_list in g:
        for file_name in file_list:
            # print(os.path.join(path, file_name))
            if os.path.splitext(file_name)[-1][1:] == "m4a":
                audioInfo = {
                    'title': os.path.splitext(file_name)[0],
                    'nickname': os.path.split(path)[1],
                    'audio_path': file_name,
                    'cover_path': '1000movies.jpg',
                    'subclass': subclass,
                }
                # print(audioInfo)
                audioInfo_list.append(audioInfo)






if __name__ == '__main__':
    # for sid in sid_list:
    #     print(f"caiji {sid}...", end='')
    #     audioInfo_list.append(caiji(sid))
    #     print('OK!')
    #     time.sleep(1)
    #
    # MONGO_DB.erge.insert_many(audioInfo_list)
    audio_path = "/Volumes/downloads/"
    wenjianjia = "[喜马拉雅]精读100本豆瓣高分电影原著"

    caiji_santi(audio_path+wenjianjia,'1000movies')
    print(audioInfo_list)
    MONGO_DB.erge.insert_many(audioInfo_list)