from flask import Blueprint, send_file,request,Response,jsonify
from setting import MONGO_DB,RET

import time
from bson import ObjectId

users = Blueprint('users',__name__)

@users.route("/reg",methods=["POST"])
def reg():
    user_info = request.form.to_dict()
    user_info['avatar'] = "mama.png" if user_info.get("gender") == "1" else "baba.png"

    user_info["friend_list"] = []
    user_info["bind_toy"] = []
    user_info["create_time"] = time.time()

    res = MONGO_DB.users.insert_one(user_info)

    RET["code"] = 0
    RET["msg"] = "用户注册成功"
    RET["data"] = {"user_id":str(res.inserted_id)}

    return jsonify(RET)

@users.route("/login",methods=["POST"])
def login():
    user_info = request.form.to_dict()
    user = MONGO_DB.users.find_one(user_info,{"password":0})
    if user:
        user["_id"] = str(user.get("_id"))

        RET['code'] = 0
    else:
        RET['code'] = -1

    RET['msg'] = '用户登录'
    RET['data'] = user

    return jsonify(RET)

@users.route("/auto_login",methods=["POST"])
def auto_login():
    print(request.form.to_dict())
    user_id = request.form.to_dict()
    user_id['_id'] = ObjectId(user_id['_id'])
    user = MONGO_DB.users.find_one(user_id,{"password":0})
    print(user)
    user["_id"] = str(user_id['_id'])

    RET['code'] = 0
    RET['msg'] = '用户自动登录'
    RET['data'] = user

    return jsonify(RET)




