from aip import AipSpeech
from setting import APP_ID,API_KEY,SECRET_KEY,VOICE,MONGO_DB
import requests,os




def text2audio(text):
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(text,'zh',1,VOICE)

    return result

def get_content(path):
    req = requests.get(path,verify=False)
    # print(req.content)
    return req.content
    # import os
    # filename = os.path.basename(path)
    # filename = os.path.join('../chats',filename)
    # print(filename)
    #
    # with open(filename, 'rb') as fp:
    #     return fp.read()

def audio2text(path):
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    filename = os.path.basename(path)
    filetype = os.path.splitext(filename)[-1][1:]
    # print(filetype)
    ret = client.asr(get_content(path),filetype,16000)

    print(ret)
    return ret
    # if ret['err_no'] == 0 :
    #     # print(ret)
    #     return ret['result'][0]
    # else:
    #     return ret['err_msg']




if __name__ == '__main__':
    # text2audio("玩具未与用户绑定，请绑定后再和我玩耍")
    #text2audio("有点小问题，请稍等")
    print(audio2text('https://192.168.8.123:8900/get_chat/tt.wav'))