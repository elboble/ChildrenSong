from flask import Blueprint, request, jsonify

from redisMsg import get_redis_one,get_redis_all,get_redis_one_toy
from setting import MONGO_DB,CHATS_SYS_PATH,ERROR_MSG,RET
from misc import _get_xxtx

from bson import ObjectId

import os

chat = Blueprint("chat", __name__)


@chat.route("/recv_msg", methods=['POST'])
def recv_msg():
    to_user = request.form.get('to_user')
    from_user = request.form.get('from_user')

    from_user,count = get_redis_one_toy(to_user, from_user)


    if MONGO_DB.users.find_one({'_id':ObjectId(from_user)}):
        friend_type = 'app'
    else:
        friend_type = 'toy'
    chat_window = MONGO_DB.chats.find_one({'user_list': {"$all": [to_user, from_user]}})

    if count:
        mychat = chat_window.get("chat_list")[-count:]
        #插入消息提示
        pre_str=_get_xxtx(to_user,from_user)
        mychat.insert(0,{'msg':pre_str})
        print(mychat)
    else:
        MSG =  os.path.join(CHATS_SYS_PATH,ERROR_MSG)
        mychat = [{'msg' : MSG}]

    # print("count:%s"%count)
    # print(mychat)
    mychat[0]['to_user'] = to_user
    mychat[0]['from_user'] = from_user
    mychat[0]['friend_type'] = friend_type
    return jsonify(mychat)

@chat.route("/chat_list", methods=['POST'])
def chat_list():
    from_user = request.form.get('from_user')
    to_user = request.form.get('to_user')
    chat_window = MONGO_DB.chats.find_one({'user_list':{"$all":[from_user,to_user]}})

    chat_l = chat_window.get("chat_list")[-10:]

    for i in range(10):
        user = MONGO_DB.users.find_one({'_id':ObjectId(chat_l[i]['from_user'])})
        if user:
            chat_l[i]['avatar']= user['avatar']
            chat_l[i]['person']='self'
        else:
            toy = MONGO_DB.toys.find_one({'_id':ObjectId(chat_l[i]['from_user'])})
            chat_l[i]['avatar'] = toy['avatar']
            chat_l[i]['person'] = ''



    #update chat badge count
    get_redis_one(from_user,to_user)

    RET['code'] = 0
    RET['msg'] = '获取历史消息'
    RET['data'] = chat_l

    return jsonify(chat_l)

@chat.route("/chat_count", methods=['POST'])
def chat_count():
    from_user = request.form.get("from_user")
    count_list = get_redis_all(from_user)

    RET['code'] = 0
    RET['msg'] = '获取未读消息数'
    RET['data']= count_list

    return jsonify(RET)