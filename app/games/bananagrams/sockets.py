from app import socketio
from app.globals import roomManager
from flask import request
from flask_socketio import emit, join_room

@socketio.on('setupbananagrams')
def setupGame(data):
    print("Setting up game")

@socketio.on('joinedGame')
def joinedGame(data):
    playerSID = request.sid
    playerID = data["playerID"]
    roomCode = data['roomCode']

    join_room(roomCode)

    print(playerID, " has joined game: ", roomCode)

    room = roomManager.getRoom(roomCode)

    room.updatePlayerSID(playerID, playerSID)
    playerData = room.game.getPlayerData(playerID)

    emit('gameData', playerData, to=playerSID)

@socketio.on('placeTileRequest')
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

@socketio.on('moveTileRequest')
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

@socketio.on('peelRequest')
def peelRequest(data):
    playerSID = request.sid
    playerID = data['playerID']
    roomCode = data["roomCode"]

    room = roomManager.getRoom(roomCode)

    if room.game.isPlayerTrayEmpty(playerID):
        playerData = room.game.getPlayerData(playerID)
        board = playerData['board']
        if room.game.areTilesConnected(board):
            words = room.game.getWords(board)
            valid, invalidWords = room.game.validateWords(words)
            
            print(valid)
            print(invalidWords)

            if not invalidWords:
                room.game.peel()

        players = room.getAllPlayers()

        for playerID, player in players.items():
            sid = player["playerSID"]
            data = room.game.getPlayerData(playerID)
            emit('gameData', data, to=sid)

    
    # if players tiles are empty
    # if all tile are connected
    # if all words are words

    # -> give every player 1 tile

@socketio.on('shiftTiles')
def shiftTiles(data):
    playerSID = request.sid
    playerID = data['playerID']
    roomCode = data["roomCode"]

    direction = data['direction']

    room = roomManager.getRoom(roomCode)

    playerData = room.game.getPlayerData(playerID)
    board = playerData['board']

    if room.game.shiftBoard(board, direction):
        data = room.game.getPlayerData(playerID)
        emit('gameData', data, to=playerSID)
    else:
        emit('error', {'message': 'Cannot shift up'}, to=playerSID)