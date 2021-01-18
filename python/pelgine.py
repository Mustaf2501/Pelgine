from flask import Flask ,render_template
import sqlite3
from python.palette_metric import   hex2Lab,extendpal
from python.tk_heap import TopKMaxHeap
import numpy as np
from heapq import *
import time
import pickle
from math import ceil


# load pixeljoint's kdtree
f = open('pixeljoint.pickle', 'rb')
tree = pickle.load(f)
app = Flask(__name__)



@app.route("/")
def home():
    # connect to Pelgine db
    conn = sqlite3.connect("pelgine.db")
    cursor = conn.cursor()

    # Example Search :  http://127.0.0.1:5000/search/pixelart/9D1D23-ff5e00-ffd914-6d2222-d94c0f
    pal = ['9D1D23', 'ff5e00', 'ffd914', '6d2222', 'd94c0f']
    pal = ["#" + color for color in pal if color != 'none']

    epal = extendpal(pal.copy(), 5)

    # search k-d tree and put results in artworks

    idurl = []
    search = hex2Lab(epal)

    results = tree.query(search, k=500, p=2)

    artworkids = {}

    for index in results[1]:
        id = int(ceil(((index + 1) / 120)))
        if id not in artworkids:
            artworkids[id] = 1
            sql = "select imgUrl from pixeljoint where rowid = {} ".format(id)
            cursor.execute(sql)
            idurl.append([id, cursor.fetchone()[0]])

    conn.close()

    ###
    return render_template("search.html", pal=[], artworks=idurl, palette=pal, numcolors=len(pal))

@app.route("/details/pixelart/<id>")
def detailspj(id):

    # connect to Pelgine db
    conn = sqlite3.connect("pelgine.db")
    cursor = conn.cursor()
    sql = "select * from pixeljoint where rowid = {} ".format(id)
    cursor.execute(sql)
    details = list(cursor.fetchone())
    conn.close()



    return  render_template("details.html", artwork= details )


@app.route("/search/pixelart/<c1>-<c2>-<c3>-<c4>-<c5>")
def searchpalette(c1,c2,c3,c4,c5):

    # connect to Pelgine db
    conn = sqlite3.connect("pelgine.db")
    cursor = conn.cursor()

    # Example Search :  http://127.0.0.1:5000/search/pixelart/9D1D23-ff5e00-ffd914-6d2222-d94c0f
    pal = [c1,c2,c3,c4,c5]
    pal = ["#"+color for color in pal if color != 'none']
    
    epal = extendpal(pal.copy(), 5)

    # search k-d tree and put results in artworks

    idurl = []
    search = hex2Lab(epal)

    results = tree.query(search, k=500, p=2)

    artworkids= {}

    for index in results[1]:
        id  = int(ceil(((index + 1) / 120)))
        if id not in artworkids:
            artworkids[id] = 1
            sql = "select imgUrl from pixeljoint where rowid = {} ".format(id)
            cursor.execute(sql)
            idurl.append([id, cursor.fetchone()[0]])

    conn.close()

    ###
    return render_template("search.html", pal=[], artworks= idurl, palette= pal, numcolors=len(pal))


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)
