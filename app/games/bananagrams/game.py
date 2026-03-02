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

        print(gameData)
        #room.addGameData(gameData)
    
    def generateTiles(self):
        return list("AAAAAAAAAAAABBBCCCDDDDEEEEEEEEEEEEEEEEEFFFGGHHHIIIIIIIIIIIJJKKLLLLMMNNNNNNNNOOOOOOOOOOOPPQRRRRRRRRRSSSSSSTTTTTTTTUUUUUUVVVWWWXXYYZZ")

    def createEmptyBoard(self, size):
        return [['' for _ in range(size)] for _ in range(size)]
    
    