"""
Multivariate Normalverteilungen
"""

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

x = np.linspace(0, 10, 100)
y = np.linspace(0, 10, 100)
X, Y = np.meshgrid(x, y)
Z = np.zeros(X.shape)

sigma = np.array([[1., 0.8], [0.8, 1.]])
mu = np.array([5., 5.]).reshape(-1, 1)
D = 2

for r, y_component in enumerate(y):
    for c, x_component in enumerate(x):
        x_vector = np.array([x_component, y_component]).reshape(-1, 1)
        Z[r, c] = 1/np.sqrt(((2*np.pi)**D) * np.linalg.det(sigma)) * \
                  np.exp(-0.5 * (x_vector-mu).T @ np.linalg.inv(sigma) @ (x_vector-mu))

fig = plt.figure("Bivariate Normalverteilung")
ax = fig.gca(projection='3d')

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
# ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("f")

# Add a color bar which maps values to colors.
# fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()