from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
import matplotlib.colors as colors
import numpy
import random

def hex2Lab(pal):

    """
    Converts a list of hexvalues to a list of Lab coordinates, as a single numpy array
    This will be used to convert the user's search into the appropriate form for searching the K-d tree

    Args:
        pal: list of hex values

    Returns:
        numpy array containing each of the colors in pal in the form of Lab coordinates.
        If pal is size (n) then the result is size (3*n)
    """

    lab_pts = []
    n = len(pal)

    for i in range(0, n):
        color_srgb = colors.hex2color(pal[i])
        color_srgb_obj = sRGBColor(color_srgb[0], color_srgb [1], color_srgb [2])
        color_lab = convert_color(color_srgb_obj, LabColor)
        lab_pts.append([color_lab.lab_l, color_lab.lab_a, color_lab.lab_b])

    lab_pal = [const for labpt in lab_pts for const in labpt]

    return numpy.array(lab_pal)


def extendpal(pal, m ):

    """
    Extends a palette to size m
    This method ensures that we can compare palettes of different sizes

    Args:
        pal: list of hexvalues
        m  : the size you want to extend pal to

    Returns:
        none
    """

    n = len(pal)
    extended_pal = pal.copy()

    for i in range(0,m-n):
        extended_pal.append(random.choice(pal)) # appends random Lab color to palette

    return extended_pal


