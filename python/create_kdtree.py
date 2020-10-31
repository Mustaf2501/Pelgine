import sqlite3
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976
import matplotlib.colors as colors
from math import sqrt
import numpy


from python.tk_heap import TopKMaxHeap
from heapq import *
import time
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pickle
import scipy.spatial
import itertools
from math import ceil

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
        lab.append( [color_lab.lab_l,color_lab.lab_a,color_lab.lab_b])

    v = [const for sublist in lab for const in sublist]
    return numpy.array(v)

urls = []
pals = []

conn = sqlite3.connect("pelgine.db")
c = conn.cursor()
c.execute("SELECT * FROM image")


for x in c:
    lab1 = [float(y) for y in x[10].split(",")]
    lab2 = [float(y) for y in x[11].split(",")]
    lab3 = [float(y) for y in x[12].split(",")]
    lab4 = [float(y) for y in x[13].split(",")]
    lab5 = [float(y) for y in x[14].split(",")]
    pal = [lab1,lab2,lab3,lab4,lab5]
    urls.append(x[9])

    itr = list(itertools.permutations(pal))

    for p in itr:
        v = [const for sublist in p for const in sublist]
        pals.append(v)




tree=scipy.spatial.cKDTree(pals)
t0 = time.time()
res = tree.query( hex2Lab(["#DB6129","#DB6129","#32958F","#32958F","#32958F"]) ,k = 500, p=2)
t1 = time.time()
d = {}
print(t1-t0)
for id in res[1]:
    index = int(ceil(((id + 1)/120))) -1
    if index not in d:
         print(urls[index])
         d[index] = 1
#raw = pickle.dumps(tree)

#with open('my_file.pickle', 'wb') as f:
    #pickle.dump(tree, f)

#with open('my_file.pickle', 'rb') as f:
    #tree = pickle.load(f)
