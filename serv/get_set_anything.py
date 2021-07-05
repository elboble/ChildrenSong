import os,re,time
import mimetypes

from uuid import uuid4

from flask import Blueprint, send_file,request,Response,jsonify

from setting import AUDIO_PATH, COVER_PATH,CHATS_PATH,RET,MONGO_DB,SERV,CHATS_COMMAND_PATH,CHATS_SYS_PATH,QR_PATH

from ai.baidu import audio2text
from ai.nlp import command_nlp

gsa = Blueprint("gsa", __name__)


@gsa.route("/get_image/<filename>")
def get_image(filename):
    cf = os.path.join(COVER_PATH, filename)
    return send_file(cf)

@gsa.route("/get_qrcode/<filename>")
def get_qrcode(filename):
    cf = os.path.join(QR_PATH, filename)
    return send_file(cf)

def partial_response(path, start, end=None):
    file_size = os.path.getsize(path)

    if end is None:
        # end = file_size - start - 1
        end = file_size - 1
    end = min(end, file_size - 1)
    length = end - start + 1

    with open(path, 'rb') as fd:
        fd.seek(start)
        bytes = fd.read(length)
    assert len(bytes) == length

    response = Response(
        bytes,
        206,
        mimetype=mimetypes.guess_type(path)[0],
        direct_passthrough=True,
    )
    response.headers.add(
        'Content-Range', 'bytes {0}-{1}/{2}'.format(
            start, file_size-1, file_size,
        ),
    )
    response.headers.add(
        'Accept-Ranges', 'bytes'
    )
    return response

def get_range(request):
    range = request.headers.get('Range')
    m = re.match('bytes=(?P<start>\d+)-(?P<end>\d+)?', range)
    if m:
        start = m.group('start')
        end = m.group('end')
        start = int(start)
        if end is not None:
            end = int(end)
        return start, end
    else:
        return 0, None


@gsa.route("/get_audio/<filename>")
def get_audio(filename):
    if 'Range' in request.headers:
        start,end = get_range(request)
        # print(start,end)
        res = partial_response(os.path.join(AUDIO_PATH,filename), start, end)
        return res

    af = os.path.join(AUDIO_PATH, filename)
    return send_file(af)


@gsa.route("/get_chat/<filename>")
def get_chat(filename):
    if 'Range' in request.headers:
        start,end = get_range(request)
        # print(start,end)
        res = partial_response(os.path.join(CHATS_PATH,filename), start, end)
        return res

    af = os.path.join(CHATS_PATH, filename)
    # print(af)
    return send_file(af)

@gsa.route("/get_chat/<path:subpath>")
def get_chat_sub(subpath):
    if 'Range' in request.headers:
        start,end = get_range(request)
        # print(start,end)
        res = partial_response(os.path.join(CHATS_PATH,subpath), start, end)
        return res

    af = os.path.join(CHATS_PATH, subpath)
    # print(af)
    return send_file(af)

@gsa.route("/uploader",methods=['POST'])
def uploader():
    audio = request.files.get("recorder")
    to_user = request.form.get('to_user')
    from_user = request.form.get('from_user')

    path = os.path.join(CHATS_PATH,audio.filename)
    audio.save(path)
    os.system(f"ffmpeg -i {path} {path}.mp3")

    #消息存储记录 chats
    # chat_window = MONGO_DB.chats.find_one({'user_list':{"$all":[to_user,from_user]}})
    msg_dict = {
        "from_user":from_user,
        "msg":f"{audio.filename}.mp3",
        "createtime":time.time()
    }
    # chat_window["chat_list"].append(msg_dict)
    # print("uploader",msg_dict)
    MONGO_DB.chats.update_one({'user_list':{"$all":[to_user,from_user]}},
                              {"$push":{'chat_list':msg_dict}})


    RET['code'] = 0
    RET['msg'] = '上传音频文件'
    RET['data'] = {"filename":f"{audio.filename}.mp3"}

    return jsonify(RET)

@gsa.route("/toy_uploader",methods=['POST'])
def toy_uploader():
    audio = request.files.get("record")
    to_user = request.form.get('to_user')
    from_user = request.form.get('from_user')
    filename = f"{uuid4()}.wav"
    path = os.path.join(CHATS_PATH,filename)
    audio.save(path)

    # os.system(f"ffmpeg -i {path} {path}.mp3")
    # os.system(f"ffmpeg -y  -i {path}  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {path}.pcm")
    # os.system(f"ffmpeg -y  -i {path}  -ac 1 -ar 16000 {path}")

    msg_dict = {
        "from_user":from_user,
        "msg":f"{filename}",
        "createtime":time.time()
    }
    # print("toy_uploader",msg_dict)

    MONGO_DB.chats.update_one({'user_list':{"$all":[to_user,from_user]}},
                              {"$push":{'chat_list':msg_dict}})

    RET['code'] = 0
    RET['msg'] = 'toy上传音频文件'
    RET['data'] = {"filename":f"{filename}"}

    return jsonify(RET)

@gsa.route("/command_uploader",methods=['POST'])
def command_uploader():
    nlp_ret = {'code':-1,"chats":None}
    audio = request.files.get("record")
    # print(audio)
    to_user = request.form.get('to_user')
    from_user = request.form.get('from_user')
    #filename = 'command/xxxx.wav'
    filename = os.path.join(CHATS_COMMAND_PATH,f"{uuid4()}.wav")
    #path = 'chats/command/xxxx.wav'
    path = os.path.join(CHATS_PATH,filename)
    audio.save(path)

    ret = audio2text(SERV+'/get_chat/'+filename)

    if ret['err_no'] == 0:
        # print(ret['result'][0])
        nlp_ret = command_nlp(ret['result'][0],from_user)
    return jsonify(nlp_ret)




    # os.system(f"ffmpeg -i {path} {path}.mp3")
    # os.system(f"ffmpeg -y  -i {path}  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {path}.pcm")
    # os.system(f"ffmpeg -y  -i {path}  -ac 1 -ar 16000 {path}")

    RET['code'] = 0
    RET['msg'] = 'toy发送指令'
    RET['data'] = {"filename":f"{filename}"}

    return jsonify(RET)

