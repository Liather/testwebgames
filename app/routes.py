from app import app
from flask import Flask, render_template

@app.route('/')
def createroom():
    return render_template('index.html')

@app.route('/room')
def room():
    return render_template('room.html')