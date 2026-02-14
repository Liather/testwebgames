from app import socketio
from flask import request
from flask_socketio import emit

@socketio.on('startBananagrams')
def setupGame(data):
    print("Setting up game")

@socketio.on('joinedGame')
def joinedGame(data):
    print("Joined game")
