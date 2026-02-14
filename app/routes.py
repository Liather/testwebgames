from app import app
from flask import Flask, render_template, send_from_directory, abort
import os

@app.route('/')
def createroom():
    return render_template('index.html')

@app.route('/room')
def room():
    return render_template('room.html')

@app.route('/game/<game>')
def game(game):
    baseDir = os.path.dirname(__file__)
    gameFolder = os.path.join(baseDir, 'games', game)
    gamePage = os.path.join(gameFolder, 'game.html')

    if os.path.exists(gamePage):
        return send_from_directory(gameFolder, 'game.html')
    else:
        abort(404)