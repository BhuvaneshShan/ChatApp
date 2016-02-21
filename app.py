from flask import *
from flask_socketio import *

from messageProcessor import *

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Bhuvanesh'
socketio = SocketIO(app)

processor = MessageProcessor()

@app.route('/')
def render():
    return render_template('index.html')

@socketio.on('userInput', namespace='/chat')
def processMessage(message):
	processor.processMessage(message)

@socketio.on('connect', namespace='/chat')
def connect():
	emit('messageToUser', {'clientName': 'Server', 'data': "Welcome to Weeby's chat server!"})
	emit('messageToUser', {'clientName': 'Server', 'data': "Login name?"})

if __name__ == '__main__':
    socketio.run(app)

