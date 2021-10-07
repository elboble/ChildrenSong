import os

from uuid import uuid4
from io import BytesIO

from ai.baidu import text2audio

from flask import Blueprint, send_file,request,Response,jsonify

from setting import AUDIO_PATH, COVER_PATH,CHATS_PATH,CHATS_SYS_PATH,ERROR_MSG

t2audio = Blueprint("t2audio", __name__)


@t2audio.route("/t2a/<text>")
def t2a(text):
    ret = text2audio(text)
    
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(ret,dict):
        return send_file(filename_or_fp=BytesIO(ret),mimetype='audio/mpeg')
    else:
        return send_file(os.path.join(CHATS_SYS_PATH,ERROR_MSG))

@t2audio.route("/t2as/<text>")
def t2as(text):
    ret = text2audio(text)

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(ret, dict):
        filename = str(uuid4())+'.mp3'
        with open(filename, 'wb') as f:
            f.write(ret)
            print(f"save {filename} OK!")
        filepath = os.path.join(CHATS_PATH, ret);
    else:
        filepath = os.path.join(CHATS_SYS_PATH,ERROR_MSG)
    return send_file(filepath)
