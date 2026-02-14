from app import socketio
from flask import request
from app.globals import roomManager, availableGames
from flask_socketio import emit, join_room

@socketio.on('createRoom_request')
def createRoomRequest(data):
    playerSID = request.sid
    playerID = data['playerID']

    if not playerID:
        emit('error', {'message': 'Missing playerID'}, to=playerSID)
        return

    room = roomManager.createRoom(playerID, playerSID)
    
    if room:
        print(playerID, " has created a room: ", room.roomCode)
        emit('roomCreated', {'roomCode': room.roomCode}, to=playerSID)
    else:
        print(playerID, " has failed to create a room: ")
        emit('error', {'message': 'Room creation failed'}, to=playerSID)

@socketio.on('joinRoom_request')
def joinRoomRequest(data):
    playerSID = request.sid
    roomCode = data['code']

    room = roomManager.getRoom(roomCode)
    
    if room:
        emit('roomFound', {'roomCode': roomCode}, to=playerSID)
    else:
        emit('error', {'message': 'Room not found'}, to=playerSID)

# ---- Room Sockets ----------------------------------------------------------------
@socketio.on('joinedRoom')
def joinedRoom(data):
    playerSID = request.sid
    playerID = data['playerID']
    roomCode = data['roomCode']
    room = roomManager.getRoom(roomCode)
    
    if room:
        print(playerID, " has joined room: ", roomCode)
    else:
        emit('error', {'message': 'Room not found'}, to=playerSID)
        return

    '''
    CHECK IF BLACKLISTED PLAYER
    '''

    # add player to room
    if not roomManager.addPlayerToRoom(roomCode, playerID, playerSID):
        emit('error', {'message': 'cant add player to room'}, to=playerSID)

    #update player sid
    if not room.updatePlayerSID(playerID, playerSID):
        emit('error', {'message': 'cant update player sid'}, to=playerSID)

    # check if valid player
    '''if not room.isPlayer(playerID):
        emit('error', {'message': 'invalidPlayer'}, to=playerSID)'''

    join_room(roomCode)

    # EMIT DATA TO ROOM
    players = room.getPlayerData()
    emit('playerData', {'players': players}, room=roomCode)

    emit('availableGames', {'availableGames': availableGames}, to=playerSID)

    selectedGame = room.getSelectedGame()
    emit('selectedGame', {'selectedGame': selectedGame}, room=roomCode)


    # GAME DATA
    # game selected
    # game settings


@socketio.on('setNicknameRequest')
def setNicknameRequest(data):
    playerSID = request.sid
    newNickname = data['newNickname']
    playerID = data['playerID']
    roomCode = data['roomCode']

    room = roomManager.getRoom(roomCode)

    if not room:
        emit('error', {'message': 'Room not found'}, to=playerSID)
        return
    
    if room.setNickname(playerID, newNickname):
        players = room.getPlayerData()
        emit('playerData', {'players': players}, room=roomCode)
    else:
        emit('error', {'message': 'Could not set nickname'}, to=playerSID)
        return

@socketio.on('setSelectedGame')
def setSelectedGame(data):
    # check if player is host
    playerID = data['playerID']
    roomCode = data['roomCode']
    selectedGame = data['selectedGame']

    room = roomManager.getRoom(roomCode)

    room.setSelectedGame(selectedGame)
    emit('selectedGame', {'selectedGame': selectedGame}, room=roomCode)

@socketio.on('startGameRequest')
def handleStartGame(data):
    playerSID = request.sid
    playerID = data["playerID"]
    roomCode = data['roomCode']
    
    room = roomManager.getRoom(roomCode)

    selectedGame = room.getSelectedGame()

    if room.isHost(playerID):
        emit('startGame', {'url': f"/game/{selectedGame}?code={roomCode}"}, room=roomCode)
    else:
        emit('error', {'message': 'You are not Host'}, to=playerSID)



'''
// playerList
    // highlight host

// gameData
    // selectedGame
    // gameConfig
        // only allow host to change game config
            // Check playerID (ifHost) when game config change request made to ensure no inspect element shananagins
'''