from flask import Blueprint, jsonify

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
    res = list(MONGO_DB.erge.find({}))
    # print(res)
    RET["code"] = 200
    RET["msg"] = "查询儿歌"
    RET["data"] = res
    return JSONEncoder().encode(RET)
