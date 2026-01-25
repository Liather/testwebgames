import os
import json
from app.roomManager import roomManager

roomManager = roomManager()

availableGames = []

def findGames():
    # look through the games folder
    # iterate through each sub directory (each game)
    # check for config.json
        # if threre, read the expected files section
        # check expected files are present
        # if all present, add to list of available games

    gamesDir = os.path.join(os.path.dirname(__file__), 'games')
    if os.path.exists(gamesDir):
        for item in os.listdir(gamesDir):
            gamesPath = os.path.join(gamesDir, item)
            if os.path.isdir(gamesPath):
                configPath = os.path.join(gamesPath, 'config.json')
                if os.path.isfile(configPath):
                    try:
                        with open(configPath, 'r') as f:
                            config = json.load(f)
                        expectedFiles = config.get('expectedFiles', [])
                        allPresent = all(os.path.isfile(os.path.join(gamesPath, file)) for file in expectedFiles)
                        if allPresent:
                            availableGames.append(item)
                    except json.JSONDecodeError:
                        pass
    print("Available Games: ", availableGames)