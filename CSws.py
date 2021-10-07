import json
from bson import ObjectId

from flask import Flask, request,jsonify
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket

from redisMsg import set_redis
from setting import PEM,KEY,MONGO_DB,RET,PROJECT_PATH
from misc import _get_xxtx


ws_app = Flask(__name__)
user_socket_dict = {}


@ws_app.route('/app/<app_id>')
def app(app_id):
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    if user_socket:
        user_socket_dict[app_id] = user_socket

    while 1:
        try:
            print("app:%s"%user_socket_dict)
            user_msg = user_socket.receive()
            # print("app%s"%user_msg)#{to_user:"toy_id",music:"asdf.mp3"}
            msg_dict = json.loads(user_msg)
            toy_socket = user_socket_dict.get(msg_dict.get("to_user"))
            msg_dict['chats'] = _get_xxtx(msg_dict.get('to_user'),msg_dict.get('from_user'))
            # print(msg_dict)
            # toy_socket.send(user_msg)
            set_redis(to_user=msg_dict.get("to_user"),from_user=msg_dict.get('from_user'))
            toy_socket.send(json.dumps(msg_dict))
        except Exception as e:
            print(e)
            RET['code'] = 0
            RET['msg'] = 'websocket链接已断开'
            RET['data'] = {}
            return jsonify(RET)


@ws_app.route('/toy/<toy_id>')
def toy(toy_id):
#    print("entering toy...")
#    print("request",request.environ)
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
#    print("user_scoket:",user_socket)
    if user_socket:
        user_socket_dict[toy_id] = user_socket

    while 1:
        try:
            print("toy:%s"%user_socket_dict)
            user_msg = user_socket.receive()
            print("toy:%s"%user_msg)

            msg_dict = json.loads(user_msg)
            print("msg_dict",msg_dict)
            app_socket = user_socket_dict.get(msg_dict.get("to_user"))

            set_redis(to_user=msg_dict.get('to_user'), from_user=msg_dict.get('from_user'))
            if not MONGO_DB.users.find_one({"_id":ObjectId(msg_dict.get('to_user'))}):
                #->toy
                msg_dict['chats'] = _get_xxtx(msg_dict.get('to_user'),msg_dict.get('from_user'))
                msg_dict['friend_type'] = 'toy'
                print(msg_dict)
                app_socket.send(json.dumps(msg_dict))
            else:
                #->app
                # print(msg_dict)
                # toy_socket.send(user_msg)
                msg_dict['friend_type'] = 'app'
                app_socket.send(json.dumps(msg_dict))
        except Exception as e:
            print(e)
            RET['code'] = 0
            RET['msg'] = 'websocket链接已断开'
            RET['data'] = {}
            return jsonify(RET)




if __name__ == '__main__':
#    http_serv = WSGIServer(('0.0.0.0', 3721), ws_app, handler_class=WebSocketHandler,certfile=PEM,keyfile=KEY)
    http_serv = WSGIServer(('0.0.0.0', 3721), ws_app, handler_class=WebSocketHandler)
try:
    http_serv.serve_forever()
except:
    pass



