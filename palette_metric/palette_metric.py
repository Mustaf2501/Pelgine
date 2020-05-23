from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976
import matplotlib.colors as colors
from math import sqrt
import numpy

# Paper : https://www.linkedin.com/in/etienne-ferrier-913012b6/


def metric(pal1, pal2):
    """
       Calculates the perceptual distance between two color palettes of the same length.

       Args:
         pal1: list containing hexadecimal color strings
         pal2: list containing hexadecimal color strings
         Example: pal1 = ['#ffffff','#bfcff2'] and pal2 = ['#a21ffb','#c6c2a2']

       Returns:
         palette_distance : float
         perceptual distance between pal1 and pal2
       """

    if len(pal1) != len(pal2):
        raise ValueError("The two palettes must be of the same size")
    else:
        n = len(pal1)  # size of both palettes
        color_distances = {}  # key: (i,j), value: color distance between pal[i] and pal[j]
        palette_distance = 0
        
        '''
        Calculates the distances between all possible pairs of colors between the two palettes
        This is an intermediate step to calculate the distance between the two palettes. 
        '''
        for i in range(0, n):
            for j in range(0, n):
                color1 = numpy.array((pal1[i][0], pal1[i][1], pal1[i][2]))
                color2 = numpy.array((pal2[j][0], pal2[j][1], pal2[j][2]))
                color_distances[(i, j)] = numpy.linalg.norm(color1-color2) # https://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy
                
        '''
        Calculates the distance between the two color palettes using the distances between the colors of each palette
        The calculated distance is the sum n best analogies between the palettes
        If an edge (i,j) is found to be among the smallest n color differences, all edges (i,m) and (n,j) are removed
        '''
        for i in range(0, n):
            min_val_edge = min(color_distances.items(), key=lambda x: x[1])  # get ((i,j), v) with smallest distance v
            palette_distance = palette_distance + min_val_edge[1]  # increase the total distance by v
            for j in list(color_distances):
                if j[0] == min_val_edge[0][0] or j[1] == min_val_edge[0][1]:
                    color_distances.pop(j, None)

        return sqrt(palette_distance)



# pal = ['#ffffff','#bfcff2']
# print(metric(pal, pal))
# print(colors.hex2color(pal[0]))
# print(colors.hex2color(pal[1]))
# print(sRGBColor(pal[0][0], pal[0][1], pal[0][2]))
# print(convert_color(sRGBColor(pal[0][0], pal[0][1], pal[0][2]), LabColor))

# print(sRGBColor(pal[1][0], pal[1][1], pal[1][2]))
# print(convert_color(sRGBColor(pal[1][0], pal[1][1], pal[1][2]), LabColor))

#LabColor (lab_l:100.0000 lab_a:-0.0005 lab_b:-0.0086) #ffffff
#LabColor (lab_l:82.9729 lab_a:1.8873 lab_b:-19.0057) #bfcff2

pal1 = numpy.array([(100.0000, -0.0005, -0.0086), (82.9729, 1.8873, -19.0057)]) # [#ffffff, #bfcff2]
pal2 = numpy.array([(100.0000, -0.0005, -0.0086), (82.9729, 1.8873, -19.0057)]) # [#ffffff, #bfcff2]
print(metric(pal1, pal2))