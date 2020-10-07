import numpy as np
import matplotlib.pyplot as plt
from bezier import *

# generate 5 (or any number that you want) random points that we want to fit (or set them youreself)
points = np.random.rand(5, 4)

# fit the points with Bezier interpolation
# use 50 points between each consecutive points to draw the curve
path = evaluate_bezier(points, 100)

# extract x & y coordinates of points
x, y = points[:,0], points[:,1]
px, py, pz, pa = path[:,0], path[:,1], path[:,2], path[:,3]

# plot
plt.figure(figsize=(11, 8))
plt.scatter(px, py, s=pz*1000.0, color="gray", alpha=0.1)
plt.plot(px, py, 'b-', alpha= 0.5)
plt.plot(x, y, 'ro')
plt.show()
