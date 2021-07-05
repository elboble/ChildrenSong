from bson import ObjectId
from flask import Blueprint, request, jsonify

from setting import MONGO_DB, RET

friends = Blueprint('friends', __name__)


@friends.route("/friend_list", methods=["POST"])
def friend_list():
    user_id = ObjectId(request.form.get('user_id'))
    user_info = MONGO_DB.users.find_one({'_id': user_id})

    # user_info['_id'] = str(user_info.get('_id'))

    RET['code'] = 0
    RET['msg'] = '获取好友列表'
    RET['data'] = user_info.get('friend_list')

    return jsonify(RET)


@friends.route("/add_req", methods=["POST"])
def add_req():
    req_info = request.form.to_dict()

    print(req_info)

    if req_info.get('friend_type') == 'app':
        user_info = MONGO_DB.users.find_one({'_id': ObjectId(req_info.get('add_user_id'))})
    else:
        user_info = MONGO_DB.toys.find_one({'_id': ObjectId(req_info.get('add_user_id'))})

    req_info['req_avatar'] = user_info.get("avatar")
    req_info['add_user_nick'] = user_info.get('nickname') if user_info.get('nickname') else user_info.get('baby_name')

    MONGO_DB.request.insert_one(req_info)

    RET['code'] = 0
    RET['msg'] = '请求添加成功'
    RET['data'] = {}

    return jsonify(RET)


@friends.route("/req_list", methods=['POST'])
def req_list():
    user_id = request.form.get('user_id')
    user_info = MONGO_DB.users.find_one({"_id": ObjectId(user_id)})
    user_bind_toy = user_info.get('bind_toy')

    req_li = list(MONGO_DB.request.find({"friend_id": {"$in": user_bind_toy}}))

    # ObjectId->Str
    for i in req_li:
        i['_id'] = str(i['_id'])

    RET['code'] = 0
    RET['msg'] = '查询好友请求'
    RET['data'] = req_li

    return jsonify(RET)


@friends.route("/ref_req", methods=["POST"])
def ref_req():
    req_id = request.form.get('req_id')
    # print(req_id)
    MONGO_DB.request.update({'_id': ObjectId(req_id)}, {"$set": {"status": 2}})

    RET['code'] = 0
    RET['msg'] = '拒绝好友请求'
    RET['data'] = {}

    return jsonify(RET)


@friends.route("/acc_req", methods=["POST"])
def acc_req():
    req_id = request.form.get('req_id')

    req_info = MONGO_DB.request.find_one({'_id': ObjectId(req_id)})

    user_info = MONGO_DB.users.find_one({'_id': ObjectId(req_info.get('add_user_id'))})
    if not user_info:
        user_info = MONGO_DB.toys.find_one({'_id': ObjectId(req_info.get('add_user_id'))})

    toy_info = MONGO_DB.toys.find_one({'_id': ObjectId(req_info.get('friend_id'))})

    chat_info = {
        'user_list': [str(user_info.get('_id')), str(toy_info.get('_id'))],
        'chat_list': []
    }
    chat_window = MONGO_DB.chats.insert_one(chat_info)
    user_add_toy = {
        "friend_id": str(toy_info.get('_id')),
        "friend_name": toy_info.get('toy_name'),
        "friend_nick": toy_info.get('baby_name'),
        "friend_avatar": toy_info.get('avatar'),
        "friend_type": "toy",
        "friend_chat": str(chat_window.inserted_id)
    }

    user_info['friend_list'].append(user_add_toy)

    toy_add_user = {
        "friend_id": str(user_info.get('_id')),
        "friend_name": user_info.get('nickname') if user_info.get('nickname') else user_info.get('baby_name'),
        "friend_nick": req_info.get('friend_remark'),
        "friend_avatar": user_info.get('avatar'),
        "friend_type": 'app' if user_info.get('nickname') else 'toy',
        "friend_chat": str(chat_window.inserted_id)
    }
    toy_info['friend_list'].append(toy_add_user)

    if user_info.get('nickname'):
        MONGO_DB.users.update_one({"_id": ObjectId(req_info.get('add_user_id'))},
                                  {'$set': user_info})
    else:
        MONGO_DB.toys.update_one({'_id': ObjectId(req_info.get('add_user_id'))},
                                 {'$set': user_info})

    MONGO_DB.toys.update_one({"_id": ObjectId(req_info.get('friend_id'))},
                             {'$set': toy_info})

    MONGO_DB.request.update_one({'_id': ObjectId(req_id)}, {"$set": {"status": 1}})

    RET['code'] = 0
    RET['msg'] = '添加好友成功'
    RET['data'] = {}

    return jsonify(RET)
