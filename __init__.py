from flask import Flask ,render_template
import sqlite3

import pickle
from math import ceil
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976
import matplotlib.colors as colors
from math import sqrt
import numpy

#from palette_metric import hex2Lab,extendpal


import random


# load pixeljoint's kdtree
f = open('pixeljoint.pickle', 'rb')
tree = pickle.load(f)
app = Flask(__name__)


def hex2Lab(pal):
    """
    Converts a list of hex values into a numpy array of Lab coordinates
    This will be used to convert the user's search into the appropriate form (Lab coordinates)

    Args:
        pal1: numpy array containing colors in Lab colors
        pal2: numpy array containing colors in Lab colors

    Returns:
        list containing the palette where each color is in LAB space

    """
    lab = []
    n = len(pal)

    for i in range(0,n):
        pal[i] = colors.hex2color(pal[i])

    for i in range(0, n):
        color_rgb = sRGBColor(pal[i][0], pal[i][1], pal[i][2])
        color_lab = convert_color(color_rgb, LabColor)
        lab.append( [color_lab.lab_l, color_lab.lab_a, color_lab.lab_b])

    v = [const for sublist in lab for const in sublist]
    return numpy.array(v)


def extendpal(pal, m ):

    """
    Extends the smaller palette to the same size as the larger one
    This method ensures that we can compare palettes of different sizes

    Args:
        pal: the small palette, which contains Lab colors
        m  : the size of the larger palette

    Returns:
        Smaller palette extended to match the size of the larger palette
    """

    n = len(pal)

    for i in range(0,m-n):
        pal.append(random.choice(pal)) # appends random Lab color to palette

    return pal


@app.route("/")
def home():
    # connect to Pelgine db
    conn = sqlite3.connect("pelgine.db")
    cursor = conn.cursor()

    # Example Search :  http://127.0.0.1:5000/search/pixelart/9D1D23-ff5e00-ffd914-6d2222-d94c0f

    pal = ['250647', 'eba834', '9a243b']
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
    #app.config['TEMPLATES_AUTO_RELOAD'] = True
    #app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    #app.run(debug=True)
    app.run()
