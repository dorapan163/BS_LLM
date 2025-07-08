# from flask import Flask, render_template
# from flask_socketio import SocketIO, emit
# import base64

# app = Flask(__name__)
# socketio = SocketIO(app)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @socketio.on('message')
# def handle_message(data):
#     # 将接收到的图像数据广播给所有连接的客户端
#     socketio.emit('image', {'data': base64.b64encode(data).decode('utf-8')})

# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=5000)


#---------------------------------可用代码

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import base64

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():

    # 从 flask 的 request 对象中获取客户端 IP 地址
    client_ip = request.remote_addr
    print(f"WebSocket 连接已建立，客户端 IP: {client_ip}")

@socketio.on('message')
def handle_message(data):
    # 将接收到的图像数据广播给所有连接的客户端
    socketio.emit('image', {'data': base64.b64encode(data).decode('utf-8')})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)