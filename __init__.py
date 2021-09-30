import sqlite3
import pickle
from math import ceil
from paletteutils import hex2Lab, extendpal
from flask import Flask ,render_template

# load kdtree of artworks from pixeljoint
f = open('pixeljoint.pickle', 'rb')
tree = pickle.load(f)
app = Flask(__name__)

@app.route("/")
def home():

    # default/homepage palette
    c1 = '250647'
    c2 = 'eba834'
    c3 = '9a243b'
    c4 = 'none'
    c5 = 'none'

    return searchpalette(c1, c2, c3, c4, c5)

@app.route("/details/pixelart/<id>")
def detailspj(id):

    # connect to Pelgine db
    conn = sqlite3.connect("pelgine.db")
    cursor = conn.cursor()

    sql = "select * from pixeljoint where rowid = {} ".format(id)
    cursor.execute(sql)

    details = list(cursor.fetchone())
    conn.close()

    return render_template("details.html", artwork= details )

@app.route("/search/pixelart/<c1>-<c2>-<c3>-<c4>-<c5>")
def searchpalette(c1,c2,c3,c4,c5):

    # connect to Pelgine db
    conn = sqlite3.connect("pelgine.db")
    cursor = conn.cursor()

    # Example Search :  http://127.0.0.1:5000/search/pixelart/9D1D23-ff5e00-ffd914-6d2222-d94c0f
    pal = [c1,c2,c3,c4,c5]
    pal = ["#"+color for color in pal if color != 'none']
    
    epal = extendpal(pal, 5)

    # search k-d tree and put results in artworks
    idurl = []
    search = hex2Lab(epal)

    results = tree.query(search, k=500, p=2)

    artworkids= {}

    for index in results[1]:
        # calculate id of artwork
        id  = int(ceil(((index + 1) / 120)))
        if id not in artworkids:
            artworkids[id] = 1
            sql = "select imgUrl from pixeljoint where rowid = {} ".format(id)
            cursor.execute(sql)
            idurl.append([id, cursor.fetchone()[0]])

    conn.close()

    return render_template("search.html", pal=[], artworks= idurl, palette= pal, numcolors=len(pal))


if __name__ == "__main__":
    app.run()
