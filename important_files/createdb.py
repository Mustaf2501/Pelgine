import json
import colorgram

import sqlite3
from python.palette_metric import hex2Lab


data = [json.loads(line) for line in open('PJ-Files/pixeldb.json', encoding='utf8')]
conn = sqlite3.connect("pelgine.db")
cursor = conn.cursor()

#print(data[0])
i = 1
for artwork in data:

    try:
        artSource = "PixelJoint"
        author = artwork['author']
        bio = ''
        title = artwork['title']
        date = str(artwork['date']['$date'])
        height = str(artwork['height'])
        width = str(artwork['width'])
        dimensions = str(height) + " x " + str(width) + " px"
        medium = "Digital"
        classification = "Pixel art"
        url = artwork['url']
        pjId = str(artwork['pjId'])
        hexlist = []

    except:
        continue

    # Extract 5 colors from an image.
    colors = colorgram.extract('C:/Users/16122/Pictures/PJ-pixels/' + pjId + url[-4:], 5)
    if len(colors) == 5:
        for c in colors:
            hexlist.append('#%02x%02x%02x' % c.rgb)
    else:
        continue


#add to db


    dbrow = tuple([i, artSource, author, bio, title, date, dimensions, medium, classification, url, hexlist[0], hexlist[1], hexlist[2], hexlist[3], hexlist[4]])
    print(dbrow)
    var_string = ', '.join('?' * len(dbrow))
    query_string = 'INSERT INTO pixeljoint VALUES (%s);' % var_string
    cursor.execute(query_string, dbrow)
    i = i + 1


conn.commit()
conn.close()
#add to kdtree

#lablist = hex2Lab(hexlist)

#print(lablist)











