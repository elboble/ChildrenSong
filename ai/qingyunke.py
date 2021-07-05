import requests,json

from setting import QINGYUNKE_URL, QINGYUNKE_PAYLOAD


def qingyunke_nlp(Q, nid):
    # http: // api.qingyunke.com / api.php?key = free & appid = 0 & msg = 播放歌曲听海
    params = QINGYUNKE_PAYLOAD
    params['msg'] = Q
    r = requests.get(QINGYUNKE_URL, params=params)
    print(r.url)
    ret = json.loads(r.content.decode('utf-8'))
    print(ret)
    if ret['result'] == 0:
        return ret['content'].replace('/','')
    else:
        return '不知道'

