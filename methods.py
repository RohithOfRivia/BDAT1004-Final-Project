import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from pymongo import MongoClient
import certifi
import json

client = MongoClient("mongodb+srv://rohith:1234@finalproject.wgqdk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client.get_database('Spotify')
records = db.Top50

def songList():
    req = requests.get("https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF")
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, 'html.parser')
        songs = soup.find_all(class_="Type__StyledComponent-sc-1ell6iv-0 bhCKIk Ballad-sc-mm6z7p-0 eTJHwt")


        tracks = []
        for i in songs:
            tracks.append(str(i))

        top50Songs = []
        for i in tracks:
            top50Songs.append(i.split("href")[1].split("\">")[1].split("</a>")[0])
        return top50Songs
        # print(top50Songs)
    else:
        print("cannot fetch songs")


def artistList():
    req = requests.get("https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF")
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, 'html.parser')
        artists = soup.find_all(class_="Type__StyledComponent-sc-1ell6iv-0 bhCKIk Mesto-sc-1e7huob-0 Row__Subtitle-sc-brbqzp-1 hTPACX gmIWQx")

        people = []
        for i in artists:
            people.append(str(i))

        top50Artists = []
        for i in people:
            top50Artists.append(i.split("href")[1].split("\">")[1].split("</a>")[0])
        return top50Artists
        # print(top50Artists)

    else:
        print("cannot fetch artists")


def updateTop50():
    while True:
        records.delete_many({})
        songs = songList()
        artists = artistList()

        data = []
        data2 = []
        counter = 1
        # for i in zip(songs, artists):
        #     data.append(i)

        for i, j in zip(songs, artists):
            print(counter, i, j)
            data2.append((counter, i, j))
            counter += 1

        print(data2)
        df = pd.DataFrame(data2, columns=['Position', 'Track', 'Artist'])
        df.index = df.index + 1

        records.insert_many(df.to_dict('records'))

        return df

        # time.sleep(20)

def trendingArtists():
    df = updateTop50()
    dfDict = df['Artist'].value_counts().head(5).to_dict()
    googleList = [["Artist", "No. of appearances in top 50"]]
    for k, v in dfDict.items():
        googleList.append([k, v])
    return googleList


# while True:
#     records.delete_many({})
#     songs = songList()
#     artists = artistList()
#
#     data = []
#     for i in zip(songs, artists):
#         data.append(i)
#
#     df = pd.DataFrame(data, columns=['Track', 'Artist'])
#     df.index = df.index + 1
#
#     records.insert_many(df.to_dict('records'))
#
#     time.sleep(20)
updateTop50()
