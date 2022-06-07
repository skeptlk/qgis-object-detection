import numpy as np
import math


# Calculate the distance between two points
def cal_dist(point_1, point_2):
    dist = np.sqrt(np.sum(np.power((point_1-point_2), 2)))
    return dist

# Calculate the azimuth of the line
def azimuthAngle(point_0, point_1):
    x1, y1 = point_0
    x2, y2 = point_1

    if x1 < x2:
        if y1 < y2:
            ang = math.atan((y2 - y1) / (x2 - x1))
            ang = ang * 180 / math.pi
            return ang
        elif y1 > y2:
            ang = math.atan((y1 - y2) / (x2 - x1))
            ang = ang * 180 / math.pi
            return 90 + (90 - ang)
        elif y1==y2:
            return 0
    elif x1 > x2:
        if y1 < y2:
            ang = math.atan((y2-y1)/(x1-x2))
            ang = ang*180/math.pi
            return 90+(90-ang)
        elif y1 > y2:
            ang = math.atan((y1-y2)/(x1-x2))
            ang = ang * 180 / math.pi
            return ang
        elif y1==y2:
            return 0

    elif x1==x2:
        return 90

