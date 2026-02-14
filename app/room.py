class Room:
    def __init__(self, roomCode, playerID, playerSID):
        self.roomCode = roomCode
        self.hostPlayerID = playerID
        self.players = {
            playerID: {
                "playerSID": playerSID,
                "playerNickname": "No nickname",
                "playerRole": "player"
            }
        }
        self.selectedGame = "No game selected"
        self.gameSettings = {}
        self.gameData = {}
    
    def isPlayer(self, playerID):
        return playerID in self.players
    
    def updatePlayerSID(self, playerID, newSID):
        if playerID in self.players:
            self.players[playerID]["playerSID"] = newSID
            return True
        return False

    def addPlayer(self, playerID, playerSID):
        self.players[playerID] = {
            "playerSID": playerSID,
            "playerNickname": "No nickname",
            "playerRole": "player"
        }

    def getPlayerData(self):
        players = []
        for player in self.players:
            players.append({
                "playerID": player,
                "playerNickname": self.players[player]["playerNickname"],
                "playerRole": self.players[player]["playerRole"],
                "isHost": player == self.hostPlayerID
            })
        return players

    def isHost(self, playerID):
        if playerID == self.hostPlayerID:
            return True
        else:
            return False
        
    def setNickname(self, playerID, newNickname):
        if playerID in self.players:
            self.players[playerID]["playerNickname"] = newNickname
            return True
        return False

    def getSelectedGame(self):
        print(self.roomCode, ": ", "selected game - ", self.selectedGame)
        return self.selectedGame

    def setSelectedGame(self, selectedGame):
        self.selectedGame = selectedGame

    def getHostName(self):
        return self.players[self.hostPlayerID]["playerNickname"]