import websocket
import json


msg = {'to_user':"toy456",'music':"asdf.mp3"}
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(1):
            time.sleep(1)
            ws.send(json.loads(msg))
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())

if __name__ == '__main__':
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://192.168.11.92:3721/",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()
