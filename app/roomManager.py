from app.room import Room
import random
import string

class roomManager:
    def __init__(self):
        self.activeRooms = {}
    
    def generateRoomCode(self, length=6):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase, k=length))
            if code not in self.activeRooms:
                return code
    
    def createRoom(self, playerID, playerSID):
        roomCode = self.generateRoomCode()
        newRoom = Room(roomCode, playerID, playerSID)
        self.activeRooms[roomCode] = newRoom
        return newRoom

    def getRoom(self, roomCode):
        return self.activeRooms.get(roomCode)
    
    def addPlayerToRoom(self, roomCode, playerID, playerSID):
        room = self.getRoom(roomCode)
        if room:
            player = room.isPlayer(playerID)
            if player:
                return True
            room.addPlayer(playerID, playerSID)
            return True
        return False