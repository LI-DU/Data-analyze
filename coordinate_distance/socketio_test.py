from flask import Flask, render_template
from flask_socketio import SocketIO,emit
from flask import Flask,jsonify
from threading import Lock
import random
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None
thread_lock = Lock()

@app.route('/')
def index():
    # return jsonify({'a':111,'b':222})
    return render_template('环形进度条.html')

@socketio.on('connect', namespace='/test_conn')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)

def background_thread():
    while True:
        socketio.sleep(5)
        t = random.randint(1, 100)
        list01 = []
        list_res = [('119.0623670', '31.6680730'), ('119.0396010', '31.6368940'), ('119.0350660', '31.6573290')]
        for i in range(len(list_res)):
            coor = {'lng': float(list_res[i][0]), 'lat': float(list_res[i][1])}
            list01.append(coor)
        dic = {'coordinate': list01}
        socketio.emit('server_response',
                      {'data': dic},namespace='/test_conn')

if __name__ == '__main__':
    socketio.run(app, debug=True)

