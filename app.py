from flask import Flask, render_template, make_response, request, jsonify
from flask_mongoengine import MongoEngine
from methods import trendingArtists
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from pymongo import MongoClient
import certifi
import json

app = Flask(__name__)

app.config["MONGODB_HOST"] = "mongodb+srv://finalproject.wgqdk.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"

db2 = MongoEngine()
db2.init_app(app)


client = MongoClient("mongodb+srv://rohith:1234@finalproject.wgqdk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client.get_database('Spotify')
records = db.Top50


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/index.html")
def index():
    return render_template("index.html")


@app.route("/top50")
def top50():
    songs = records.find({})
    return render_template('Top50.html', songs=songs)


@app.route("/trendingArtists")
def trending():
    data = trendingArtists()
    print(data)
    return render_template("trendingArtists.html", data=data)


@app.route("/trendingArtists2")
def trending2():
    data = trendingArtists()
    print(data)
    return render_template("trendingArtists2.html", data=data)


class Song(db2.Document):
    Position = db2.IntField()
    Track = db2.StringField()
    Artist = db2.StringField()

    def to_json(self):
        return {
            "Position": self.Position,
            "Track": self.Track,
            "Artist": self.Artist
        }


@app.route("/api/songs", methods=['Get'])
def getAll():
    if request.method == "GET":
        songs = []
        for song in Song.objects:
            songs.append(song)
        return make_response(jsonify(songs), 200)


@app.route("/api/songs/<Position>", methods=['Get'])
def getOne():
    if request.method == "GET":
        pass

@app.route("/api/songs/<range>", methods=['Get'])
def getSome():
    if request.method == "GET":
        pass


if __name__ == "__main__":
    app.run(debug=True)