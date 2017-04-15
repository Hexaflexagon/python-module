"""World library with useful calculations for the GTA Orange Python wrapper
"""
import math


def getDistance(x1, y1, z1, x2, y2=None, z2=None):
    """Returns the distance between two points, either 3-dimensional ones or 2-dimensional ones.

    Please use the components of them in a row as parameters.
    For example, if you've 2d points:

        A(10|20), B(30|40)
        getDistance(10, 20, 30, 40)

    And if you've 3d points:

        C(50|60|70), D(80|90|100)
        getDistance(50, 60, 70, 80, 90, 100)

    @param  x1      float   x-coord of first point
    @param  y1      float   y-coord of first point
    @param  z1      float   z-coord of first point
    @param  x2      float   x-coord of second point
    @param  y2      float   y-coord of second point #optional
    @param  z2      float   z-coord of second point #optional

    @returns    float   distance between given points
    """
    if y2 is None:
        return math.sqrt(math.pow(z1 - x1, 2) + math.pow(x2 - y1, 2))
    else:
        return math.sqrt(math.pow(x1 - x1, 2) + math.pow(y2 - y1, 2) + math.pow(z2 - z1, 2))
