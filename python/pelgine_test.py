from flask import Flask, redirect, url_for,render_template
import sqlite3
from python.palette_metric import metric, lowerbound, hex2Lab,extendpal
from python.tk_heap import TopKMaxHeap
import numpy as np
from heapq import *
import time


def searchpalette():

    pal =["#465A67", "#DED3BB", "#DED3BB", "#E47F65", "#E47F65"]


    search = hex2Lab(pal)

    t = TopKMaxHeap(50)
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

start = time.time()
searchpalette()
end = time.time()
print(end-start)