from flask import Flask ,render_template
import sqlite3
from python.palette_metric import   hex2Lab,extendpal
from python.tk_heap import TopKMaxHeap
import numpy as np
from heapq import *
import time


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("frontpage.html")



@app.route("/search/<palette>")
def searchpalette(palette):

    t0 = time.time()
    p = ["#465A67", "#DED3BB", "#DED3BB", "#E47F65", "#E47F65"]
    extendpal(p,5)
    search = hex2Lab( p )

    t = TopKMaxHeap(20)
    conn = sqlite3.connect("pelgine.db")
    c = conn.cursor()
    c.execute("SELECT * FROM image")

    for x in c:
        lab1 = [float(y) for y in x[10].split(",")]
        lab2 = [float(y) for y in x[11].split(",")]
        lab3 = [float(y) for y in x[12].split(",")]
        lab4 = [float(y) for y in x[13].split(",")]
        lab5 = [float(y) for y in x[14].split(",")]

        pal = np.array([lab1,lab2,lab3,lab4,lab5])

        t.push(x[9], pal, search)

    best_art = nlargest(t.k, t.maxheap)
    print(best_art)

    conn.close()


    t1 = time.time()
    print(t1-t0)



    return render_template("extendtest.html")


if __name__ == "__main__":
    app.run(debug=True)