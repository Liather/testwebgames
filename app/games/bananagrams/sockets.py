from app import socketio
from flask import request
from flask_socketio import emit

@socketio.on('setupbananagrams')
def setupGame(data):
    print("Setting up game")

@socketio.on('joinedGame')
def joinedGame(data):
    playerSID = request.sid
    playerID = data["playerID"]
    roomCode = data['roomCode']

    print(playerID, " has joined game: ", roomCode)