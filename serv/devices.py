from bson import ObjectId
from flask import Blueprint, request, jsonify

from setting import MONGO_DB, RET

devices = Blueprint('devices', __name__)


@devices.route("/validate_code", methods=["POST"])
def validata_code():
    code = request.form.to_dict()

    res = MONGO_DB.devices.find_one(code, {'_id': 0})

    if res:
        toy = MONGO_DB.toys.find_one(code)
        if toy:
            RET['code'] = 1
            RET['msg'] = '设备已绑定，添加好友'
            toy['_id'] = str(toy['_id'])
            RET['data'] = toy
        else:
            RET['code'] = 0
            RET['msg'] = '设备已授权，开启绑定'
            RET['data'] = res
    else:
        RET['code'] = 2
        RET['msg'] = '非授权设备'
        RET['data'] = {}

    print(RET)
    return jsonify(RET)


@devices.route('/bind_toy', methods=['POST'])
def bind_toy():
    # 1.device_key 2.formdata 3.who bind toy
    toy_info = request.form.to_dict()
    # 创建聊天窗口
    chat_window = MONGO_DB.chats.insert_one({'user_list': [], 'chat_list': []})

    user_info = MONGO_DB.users.find_one({'_id': ObjectId(toy_info['user_id'])})

    toy_info['bind_user'] = toy_info.pop('user_id')
    toy_info['avatar'] = 'toy.jpg'
    # 自然逻辑 好友关系
    toy_info['friend_list'] = [
        {
            'friend_id': toy_info['bind_user'],
            'friend_name': user_info.get('nickname'),
            'friend_nick': toy_info.pop("remark"),
            'friend_avatar': user_info.get("avatar"),
            'friend_type': "app",
            'friend_chat': str(chat_window.inserted_id)
        }
    ]

    toy = MONGO_DB.toys.insert_one(toy_info)

    """
        {
        "_id" : ObjectId("6094d4525d824a29d4b3b5ed"),
        "username" : "bunny",
        "password" : "202cb962ac59075b964b07152d234b70",
        "nickname" : "小兔",
        "gender" : "2",
        "avatar" : "baba.png",
        "friend_list" : [
            {
                "friend_id" : "6097e4e9f43e38850860a5fd",
                "friend_name" : "流氓兔",
                "friend_nick" : "肥宅",
                "friend_avatar" : "toy.jpg",
                "friend_type" : "toy",
                "friend_chat" : "6097e4e9f43e38850860a5fc"
            },
            {
                "friend_id" : "609a951bb7440f5495b2928a",
                "friend_name" : "吗卡巴卡",
                "friend_nick" : "肥仔",
                "friend_avatar" : "toy.jpg",
                "friend_type" : "toy",
                "friend_chat" : "609a951bb7440f5495b29289"
            }
        ],
        "bind_toy" : [
            "6097e4e9f43e38850860a5fd",
            "609a951bb7440f5495b2928a"
        ],
        "create_time" : 1620366418.589964
        },
    """
    user_info['bind_toy'].append(str(toy.inserted_id))
    user_add_toy = {
        'friend_id': str(toy.inserted_id),
        'friend_name': toy_info.get('toy_name'),
        'friend_nick': toy_info.get("baby_name"),
        'friend_avatar': toy_info.get("avatar"),
        'friend_type': "toy",
        'friend_chat': str(chat_window.inserted_id)
    }
    user_info['friend_list'].append(user_add_toy)

    MONGO_DB.users.update_one({'_id': ObjectId(toy_info['bind_user'])}, {"$set": user_info})
    MONGO_DB.chats.update_one({'_id': chat_window.inserted_id},
                              {"$set": {"user_list": [str(toy.inserted_id), str(user_info.get('_id'))]}})

    RET['code'] = 0
    RET['msg'] = '绑定玩具成功'
    RET['data'] = {}

    return jsonify(RET)


@devices.route('/toy_list', methods=['POST'])
def toy_list():
    user_id = request.form.get('user_id')
    user_info = MONGO_DB.users.find_one({'_id': ObjectId(user_id)})
    user_bind_toy = user_info.get('bind_toy')
    for index, item in enumerate(user_bind_toy):
        user_bind_toy[index] = ObjectId(item)

    toy_l = list(MONGO_DB.toys.find({'_id': {"$in": user_bind_toy}}))
    # print(toy_l)
    for index, toy in enumerate(toy_l):
        toy_l[index]['_id'] = str(toy.get('_id'))

    RET['code'] = 0
    RET['msg'] = '查看所有玩具'
    RET['data'] = toy_l

    return jsonify(RET)


@devices.route('/device_login', methods=['POST'])
def device_login():
    dev_key = request.form.to_dict()

    print(dev_key)
    # dev_key['device_key']=ObjectId(dev_key['device_key'])
    ret = MONGO_DB.devices.find_one(dev_key)

    if ret:  # 合法玩具序列号
        ret = MONGO_DB.toys.find_one(dev_key)
        if ret:  # 已绑定
            ret['_id'] = str(ret['_id'])
            # print(ret)
            RET['code'] = 0
            RET['msg'] = '我是'+ret['toy_name']+',欢迎进入小兔的亲子世界'

            RET['data'] = ret
        else:  # 未绑定
            RET['code'] = 2
            RET['msg'] = '玩具未与用户绑定，请绑定后再和我玩耍'
            RET['data'] = {}
    else:  # 非法玩具序列号
        RET['code'] = -1
        RET['msg'] = '玩具序列号有误，请联系玩具经销商'
        RET['data'] = {}

    return jsonify(RET)
