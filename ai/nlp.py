import re

from bson import ObjectId
from pypinyin import lazy_pinyin, TONE2

from ai.qingyunke import qingyunke_nlp
from setting import MONGO_DB
from ai.my_simnet import do_simnet


def command_nlp(Q, nid):
    ts = "不懂你在说什么"
    from_user = 'ai'
    friend_type = ''
    print("Q:", Q)
    if '发消息' in Q:
        pinyin_Q = "".join(lazy_pinyin(Q, style=TONE2))
        toy = MONGO_DB.toys.find_one({'_id': ObjectId(nid)})
        for friend in toy.get('friend_list'):
            nick = friend.get('friend_nick')
            name = friend.get('friend_name')
            pinyin_nick = "".join(lazy_pinyin(nick, style=TONE2))
            pinyin_name = "".join(lazy_pinyin(name, style=TONE2))
            if pinyin_nick in pinyin_Q or pinyin_name in pinyin_Q:
                ts = f"可以按消息健给{nick if nick  else name}发消息"
                from_user = friend.get('friend_id')
                friend_type = friend.get('friend_type')
                break
        else:
            ts = "可以按消息健给陌生人发消息"
            from_user = 'ai'
    elif '要听' in Q or '想听' in Q or '播放' in Q:
        title = do_simnet(Q)
        if title:
            erge = MONGO_DB.erge.find_one({"title":title})
            return {'code': 0, 'music': erge.get('audio_path'), 'from_user': 'ai'}
        else:
            return {'code': 0, 'chats': 'error.mp3' ,'from_user' :'ai'}
    else:
        ts = qingyunke_nlp(Q, nid)
        ts = re.sub(r'(\{.*\})', '', ts)

    chats = {'code': 0, "chats": ts, "from_user": from_user,"friend_type":friend_type}
    return chats


