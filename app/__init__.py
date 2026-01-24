from flask import Flask
from flask_socketio import SocketIO
#from app.globals import findGames

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#findGames()

from app import routes, sockets