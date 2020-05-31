from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976
import matplotlib.colors as colors
from math import sqrt
import numpy
import time
from PIL import Image

# Paper : https://www.linkedin.com/in/etienne-ferrier-913012b6/

def hex2Lab(pal):
    """
    Converts a list of hex values into a numpy array of Lab coordinates
    This will be used to convert the user's search into the appropriate form (Lab coordinates)

    Args:
        pal1: numpy array containing colors in Lab colors
        pal2: numpy array containing colors in Lab colors

    Returns:
        lower bound on distance between pal1 and pal2: float

    """
    lab = []
    n = len(pal)

    for i in range(0,n):
        pal[i] = colors.hex2color(pal[i])

    for i in range(0, n):
        color_rgb = sRGBColor(pal[i][0], pal[i][1], pal[i][2])
        color_lab = convert_color(color_rgb, LabColor)
        lab.append( [color_lab.lab_l,color_lab.lab_a,color_lab.lab_b])

    return numpy.array(lab)


def lowerbound(pal1,pal2):
    """
     Calculates the lower bound on perceptual distance between two color palette
     This calculation is computationally cheaper than metric(pal1,pal2), and we can use it to filter artworks

     Args:
         pal1: numpy array containing colors in Lab colors
         pal2: numpy array containing colors in Lab colors

     Returns:
        lower bound on distance between pal1 and pal2: float
     """
    n = len(pal1)
    sumx = numpy.array([0,0,0])
    sumy = numpy.array([0,0,0])

    for i in range(0, n):
        sumx = numpy.add(sumx,pal1[i])
        sumy = numpy.add(sumy, pal2[i])

    sumx = (1/n)*sumx
    sumy = (1/n)*sumy

    subxy = numpy.subtract(sumx,sumy)

    return (sqrt(n))*numpy.linalg.norm(subxy)

def metric(pal1, pal2):
    """
    Calculates the perceptual distance between two color palettes of the same length.

    Args:
        pal1: numpy array containing colors in Lab colors
        pal2: numpy array containing colors in Lab colors

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
                color1 = pal1[i]
                color2 = pal2[j]
                color_distances[(i, j)] = numpy.linalg.norm(color1-color2)**2  # https://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy
                
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
