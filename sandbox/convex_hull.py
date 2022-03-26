import numpy as np
from scipy.spatial import ConvexHull

points = np.array([[1, 4, 7, 5],
                   [4, 0, 9, 5],
                   [6, 2, 1, 5],
                   [0, 3, 5, 5],
                   [4, 5, 3, 5],
                   [3, 9, 4, 5],
                   [4, 9, 4, 9],
                   [6, 9, 4, 5],
                   [3, 5, 4, 5]])
# points = np.array([[1, 2, 3],
#                    [4, 50, 6],
#                    [7, 8, 9],
#                    [10, 12, 16]])

hull = ConvexHull(points=points)
print(hull.points)
print(hull.volume)
