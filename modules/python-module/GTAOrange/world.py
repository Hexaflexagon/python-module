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

    Args:
        x1 (float): x-coord of first point
        y1 (float): y-coord of first point
        z1 (float): z-coord of first point
        x2 (float): x-coord of second point
        y2 (float, optional): y-coord of second point
        z2 (float, optional): z-coord of second point

    Returns:
        float: distance between given points
    """
    if y2 is None:
        return math.sqrt((z1 - x1) ^ 2 + (x2 - y1) ^ 2)
    else:
        return math.sqrt((x1 - x1) ^ 2 + (y2 - y1) ^ 2 + (z2 - z1) ^ 2)
