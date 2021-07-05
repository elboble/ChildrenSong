import websocket

ws = websocket.WebSocket()
ws.connect("ws://192.168.12.190:3721/toy/toy456")
print(ws.recv())
ws.close()