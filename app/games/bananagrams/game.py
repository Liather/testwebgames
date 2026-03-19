from app.globals import roomManager
import random

TILES_PER_PLAYER = 21
BOARD_SIZE = 20

class Game:
    def __init__(self, room):
        self.room = room
        self.setupGame()

    def setupGame(self):
        tiles = self.generateTiles()
        random.shuffle(tiles)

        gameData = {
            "global": {
                "tilesRemaining": tiles,
            },
            "players": {},
        }

        room = roomManager.getRoom(self.room.roomCode)
        players = room.getPlayerData()
    

        for player in players:
            playerID = player["playerID"]
            playerTiles = tiles[:TILES_PER_PLAYER]

            tiles = tiles[TILES_PER_PLAYER:]

            gameData["players"][playerID] = {
                "board": self.createEmptyBoard(BOARD_SIZE),
                "tileTray": playerTiles
            }

        self.room.addGameData(gameData)
        print("Room: ", self.room)
    
    def generateTiles(self):
        return list("AAAAAAAAAAAABBBCCCDDDDEEEEEEEEEEEEEEEEEFFFGGHHHIIIIIIIIIIIJJKKLLLLMMNNNNNNNNOOOOOOOOOOOPPQRRRRRRRRRSSSSSSTTTTTTTTUUUUUUVVVWWWXXYYZZ")

    def createEmptyBoard(self, size):
        return [["" for _ in range(size)] for _ in range(size)]

    #def test(self):
        #print(self.room.gameData)

    def getPlayerData(self, playerID):
        gameData = self.room.gameData

        return {
            "tileTray": gameData["players"][playerID]["tileTray"],
            "board": gameData["players"][playerID]["board"]
        }

    def placeTile(self, playerID, x, y, tile):
        self.room.gameData['players'][playerID]['board'][y][x] = tile
    
    def removeTile(self, playerID, x, y, tile):
        self.room.gameData['players'][playerID]['board'][y][x] = ''

    # PLACE TILE LOGIC
    def tryPlaceTile(self, playerID, trayIndex, x, y):
        data = self.getPlayerData(playerID)
        selectedTile = data['tileTray'][trayIndex]
        cell = data['board'][y][x]

        if (cell == ''):
            self.placeTile(playerID, x, y, selectedTile)
            data['tileTray'].pop(trayIndex)
            return True
        else:
            return False

    # MOVE TLIE LOGIC
    def tryMoveTile(self, playerID, fromX, fromY, toX, toY):
        data = self.getPlayerData(playerID)
        fromCell = data['board'][fromY][fromX]
        toCell = data['board'][toY][toX]

        if (toCell == ''):
            self.placeTile(playerID, toX, toY, fromCell)
            self.removeTile(playerID, fromX, fromY, fromCell)
            return True
        else:
            return False