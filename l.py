import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='2d')

# X = [70, 75, 45, 80, 52, 64, 30, 60, 54, 65]
# Y = [25, 43, 17, 88, 37, 31, 44, 21, 51, 18]
# Z = [1, 1, 2, 1, 2, 1, 2, 2, 1, 2]

X = [25, 43, 88, 31, 51]
Y = [70, 75, 80, 64, 54]

Xs = [17, 37, 44, 21, 18]
Ys = [45, 52, 30, 60, 65]

# plt.scatter(Y,Xs,Ys, label="alpha", color='k')
ax.scatter(X, Y, c='r', marker='o')
ax.scatter(Xs, Ys, c='b', marker='^')
#
# print(len(X), len(Y))
# plt.savefig('alpha.jpg')
plt.show()
