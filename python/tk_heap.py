from heapq import *
from palette_metric import metric, lowerbound, hex2Lab
from PIL import Image
import numpy
import time


class TopKMaxHeap:
    """
    Data structure to manage the top K closest artworks to the search color palette

    Fixed-size max heap

    Each node in the heap has (id,val), where id is the identification for the artwork and val is the distance
    from the search palette, in terms of the color palette metric
    """
    def __init__(self, k):

        self.size = 0  # current size
        self.k = k   # limit for size of max heap
        self.maxheap = []

    def push(self, artID, pal, search):
        if self.size < self.k:
            heappush(self.maxheap, (-1*metric(search, pal), artID))
            self.size = self.size + 1
        else:
            root_dist = self.maxheap[0][0]

            if -1*lowerbound(search, pal) > root_dist:
                distance = -1*metric(search, pal)
                if distance > root_dist:
                    heapreplace(self.maxheap, (distance, artID))




""" 
search =  hex2Lab(['#2B412A', '#4C9307', '#8B9E37', '#A2A53D', '#9A8136'])

t = TopKMaxHeap(10)

start = time.time()
with open('palettes2.txt') as f:
    for line in f:
        p = [float(x) for x in line.split()]
        pal = numpy.array([[p[1],p[2],p[3]],[p[4],p[5],p[6]],[p[7],p[8],p[9]],[p[10],p[11],p[12]],[p[13],p[14],p[15]]])
        t.push(p[0], pal, search)

end = time.time()
print(end-start)
best_art = nlargest(t.k, t.maxheap)

print(best_art)
for i in range(t.k):
    im = Image.open("demo_art/" + str(int(best_art[i][1])) + '.png')
    im.show()
"""
