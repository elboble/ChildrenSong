from setting import REDIS_DB
import json

'''
{to_user:
    {from_user1:1},
    {from_user2:1},
    {from_user3:2},
    ...
}    
'''


def set_redis(to_user, from_user):
    # print("set_redis %s,%s"%(to_user,from_user))
    to_user_msg = REDIS_DB.get(to_user)
    if to_user_msg:
        to_user_msg = json.loads(to_user_msg)
        if to_user_msg.get(from_user):
            to_user_msg[from_user] += 1
        else:
            to_user_msg[from_user] = 1
    else:
        to_user_msg = {from_user: 1}

    REDIS_DB.set(to_user, json.dumps(to_user_msg))


# set_redis("toy", 'app')


def get_redis_one(to_user, from_user):
    to_user_msg = REDIS_DB.get(to_user)
    if to_user_msg:
        to_user_msg = json.loads(to_user_msg)
        count = to_user_msg.get(from_user, 0)

        to_user_msg[from_user] = 0
        # print(count)
        REDIS_DB.set(to_user, json.dumps(to_user_msg))
        return count
    else:
        return 0


def get_redis_one_toy(to_user, from_user):

    to_user_msg = REDIS_DB.get(to_user)

    if to_user_msg:
        to_user_msg = json.loads(to_user_msg)
        count = to_user_msg.get(from_user, 0)
        if count == 0:
            for key, value in to_user_msg.items():
                if value != 0:
                    count = value
                    from_user = key
                    break

        print(from_user, count)
        to_user_msg[from_user] = 0
        # print(count)
        REDIS_DB.set(to_user, json.dumps(to_user_msg))
        return from_user, count
    else:
        return from_user, 0


# 首页未读好友消息数字上标的接口，所以不set_redis
def get_redis_all(nid):
    msg_dict = REDIS_DB.get(nid)

    if msg_dict:
        msg_dict = json.loads(msg_dict)

        # print(msg_dict)
        count = sum(msg_dict.values())
        # print(count)
        # for key,value in msg_dict.items():
        #     count += value

        msg_dict['count'] = count
        #
        # for k,v in msg_dict.items():
        #     # d = {}
        #     # d[k]=v
        #     msg_list.append({k:v})
        # msg_dict['sub']=msg_list
        return msg_dict
    else:
        return 0
