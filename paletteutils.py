from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
import matplotlib.colors as colors
import numpy
import random

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
