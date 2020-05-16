from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976
import matplotlib.colors as colors

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
        Converts each hexadecimal color value (within each palette) into a sRGB triplet
        This step is needed so that we later convert the sRGB triplets into LAB for comparison with delta_e_cie1976
        '''
        for i in range(0, n):
            pal1[i] = colors.hex2color(pal1[i])
            pal2[i] = colors.hex2color(pal2[i])

        '''
        Calculates the distances between all possible pairs of colors between the two palettes
        This is an intermediate step to calculate the distance between the two palettes. 
        '''
        for i in range(0, n):
            for j in range(0, n):
                color1_rgb = sRGBColor(pal1[i][0], pal1[i][1], pal1[i][2])
                color2_rgb = sRGBColor(pal2[j][0], pal2[j][1], pal2[j][2])
                color1_lab = convert_color(color1_rgb, LabColor)
                color2_lab = convert_color(color2_rgb, LabColor)
                color_distances[(i, j)] = delta_e_cie1976(color1_lab, color2_lab)

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

        return palette_distance