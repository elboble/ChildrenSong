import paginate as paginate
from flask import Blueprint, jsonify,request


from setting import MONGO_DB, RET

content = Blueprint("content", __name__)

import json
from bson import ObjectId

page_res = []

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@content.route("/content_list",methods=["POST"])
def content_list():
    subclass = request.form.get('subclass')
    res = list(MONGO_DB.erge.find({'subclass':subclass}).sort('title',1))
    # print(res)
    RET["code"] = 200
    RET["msg"] = "查询儿歌"
    RET["data"] = res
    return JSONEncoder().encode(RET)


@content.route("/content_list_p",methods=["POST"])
def content_list_p():
    subclass = request.form.get('subclass')
    page_size = int(request.form.get('page_size'))
    limit_start = int(request.form.get('limit_start',0))
    # if limit_start == 0:
    #     page_res = []
    res = list(MONGO_DB.erge.find({'subclass':subclass}).sort('title', 1).limit(page_size).skip(limit_start))
    # print(res)
    # page_res.extend(res)
    # print(page_res)
    RET["code"] = 200
    RET["msg"] = "查询儿歌"
    RET["data"] = res
    return JSONEncoder().encode(RET)
