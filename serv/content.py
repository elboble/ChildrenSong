from flask import Blueprint, jsonify,request


from setting import MONGO_DB, RET

content = Blueprint("content", __name__)

import json
from bson import ObjectId

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
