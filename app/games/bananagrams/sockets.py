from app import socketio
from app.globals import roomManager
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

    room = roomManager.getRoom(roomCode)

    playerData = room.game.getPlayerData(playerID)

    emit('gameData', playerData, to=playerSID)

@socketio.on('placeTile')
def placeTile(data):
    playerSID = request.sid
    playerID = data["playerID"]
    roomCode = data["roomCode"]

    trayIndex = data["trayIndex"]
    x = data["x"]
    y = data["y"]

    room = roomManager.getRoom(roomCode)

    test = room.game.tryPlaceTile(playerID, trayIndex, x, y)

    if test:
        playerData = room.game.getPlayerData(playerID)
        emit('gameData', playerData, to=playerSID)
    else:
        emit('error', {'message': 'No game selected'}, to=playerSID)

@socketio.on('moveTile')
def moveTile(data):
    playerSID = request.sid
    playerID = data["playerID"]
    roomCode = data["roomCode"]

    fromX = data["fromX"]
    fromY = data["fromY"]
    toX = data["toX"]
    toY = data["toY"]
    
    room = roomManager.getRoom(roomCode)

    test = room.game.tryMoveTile(playerID, fromX, fromY, toX, toY)

    if test:
        playerData = room.game.getPlayerData(playerID)
        emit('gameData', playerData, to=playerSID)
    else:
        emit('error', {'message': 'No game selected'}, to=playerSID)