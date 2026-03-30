from app.globals import roomManager
import random

TILES_PER_PLAYER = 5
BOARD_SIZE = 15

class Game:
    def __init__(self, room):
        self.room = room
        self.setupGame()
        self.dictionary = self.loadDictionary()
        
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

    def getPlayerData(self, playerID):
        gameData = self.room.gameData

        return {
            "tileTray": gameData["players"][playerID]["tileTray"],
            "board": gameData["players"][playerID]["board"]
        }
    
    def isPlayerTrayEmpty(self, playerID):
        if (self.room.gameData['players'][playerID]['tileTray'] == []):
            return True
        else:
            return False

    def peel(self):
        gameData = self.room.gameData
        tilesRemaining = gameData['global']['tilesRemaining']

        if len(tilesRemaining) < 10:
            return False

        players = gameData['players']

        for playerID in players:
            tile = tilesRemaining.pop(0)
            players[playerID]['tileTray'].append(tile)
        
        return True

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

    def loadDictionary(self):
            with open("app/games/bananagrams/dictionary.txt", "r") as f:
                return set(word.strip().upper() for word in f)

    def areTilesConnected(self, board):
        size = len(board)
        
        visited = set()
        totalTiles = 0
        start = None

        for y in range(size):
            for x in range(size):
                if board[y][x] != "":
                    totalTiles += 1
                    if start is None:
                        start = (x, y)

        if totalTiles == 0:
            return False

        stack = [start]

        while stack:
            x, y = stack.pop()

            if (x, y) in visited:
                continue

            visited.add((x, y))

            for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                nx, ny = x + dx, y + dy

                if 0 <= nx < size and 0 <= ny < size:
                    if board[ny][nx] != "" and (nx, ny) not in visited:
                        stack.append((nx, ny))

        return len(visited) == totalTiles

    def getWords(self, board):
        size = len(board)
        words = []

        # HORRIZONTAL WORDS
        for y in range(size):
            currentWord = ""

            for x in range(size):
                if board[y][x] != "":
                    currentWord += board[y][x]
                else:
                    if len(currentWord) > 1:
                        words.append(currentWord)
                    currentWord = ""

            if len(currentWord) > 1:
                words.append(currentWord)

        # VERTICAL WORDS
        for x in range(size):
            currentWord = ""

            for y in range(size):
                if board[y][x] != "":
                    currentWord += board[y][x]
                else:
                    if len(currentWord) > 1:
                        words.append(currentWord)
                    currentWord = ""

            if len(currentWord) > 1:
                words.append(currentWord)

        return words

    def validateWords(self, words):
        invalidWords = []

        for word in words:
            if word.upper() not in self.dictionary:
                invalidWords.append(word)

        if invalidWords:
            return False, invalidWords

        return True, []