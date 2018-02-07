import numpy as np
from matplotlib import pyplot, animation

fig = pyplot.figure(num=None, figsize=(8, 6), dpi=120)


def init_data(xtras=0):
    # x = np.zeros((160, 160))
    x = np.random.choice([0, 1], (260, 260), p=[.85, .15])
    y = np.lib.pad(x, 32, 'constant', constant_values=0)
    np.random.shuffle(y)
    y = np.transpose(y)
    np.random.shuffle(y)
    if xtras != 0:
        glider_attack(y, xtras)
    z = np.lib.pad(y, 16, 'constant', constant_values=0)
    return z


def glider_attack(victim, num):
    # Outline for the darn gliders
    gl = np.array([[0, 0, 1],
                   [1, 0, 1],
                   [0, 1, 1]])
    for g in range(num):
        # Pick some spots to put some f'n gliders
        x = np.random.randint(16, 200)
        y = np.random.randint(16, 200)
        # Insert (parasitically) glider into the world
        victim[x:x + 3, y:y + 3] = gl


def iterate(Z):
    # Count neighbors
    n = (Z[0:-2, 0:-2] + Z[0:-2, 1:-1] + Z[0:-2, 2:] +
         Z[1:-1, 0:-2] + Z[1:-1, 2:] +
         Z[2:, 0:-2] + Z[2:, 1:-1] + Z[2:, 2:])
    # Apply rules
    birth = (n == 3) & (Z[1:-1, 1:-1] == 0)
    survive = ((n == 2) | (n == 3)) & (Z[1:-1, 1:-1] == 1)
    Z[...] = 0
    Z[1:-1, 1:-1][birth | survive] = 1
    if np.count_nonzero(Z) < 200:  # Change this to a big number to watch glider invasion
        glider_attack(Z, 1)
    return Z

# Begin
Z = init_data(7) # int is how many darn gliders to add

img = pyplot.imshow(Z, interpolation='nearest', animated=True)
pyplot.axis('off')
pyplot.set_cmap('gnuplot')
pyplot.tight_layout()


def update_plot(*args):
    iterate(Z)
    img.set_array(Z)
    return img,

anime = animation.FuncAnimation(fig, update_plot, interval=30, blit=True)
pyplot.show()




