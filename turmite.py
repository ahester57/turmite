# Austin Hester 09/26/16
# turmite thing
# quite termity
# NEW(9.28.16):
#   - More efficient, uses 2-D arrays of tuples as rule set rather than bunch of if's
#   - Bounds checking, wraps around when out of bounds
#   - Pick your turmite from options dict
#   - cleaned up code
#
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
import pylab
import time 

fig = plt.figure(num=None, figsize=(8, 6), dpi=90)


class Turmite:

    def __init__(self, loc, x, r):
        self.i = loc[0]
        self.j = loc[1]
        self.state = 0
        self.color = x[loc[0], loc[1]]
        x[loc[0], loc[1]] = 2
        self.turn = 0
        self.rules = r

    def move(self, x):
        # Functions for movement
        def go_up():
            self.i -= 1

        def go_right():
            self.j += 1

        def go_down():
            self.i += 1

        def go_left():
            self.j -= 1

        # Dictionaries for movement
        dirs = {0: go_up,
                90: go_right,
                180: go_down,
                270: go_left}

        turn = {1: 0,
                2: 90,
                4: 180,
                8: -90}

        # initiate data for this move
        data = self.rules[self.state, self.color]

        write_color = data[0]
        self.turn += turn[data[1]]
        next_state = data[2]

        # Directions bounded [0, 360]
        if self.turn > 270:
            self.turn -= 360
        elif self.turn < 0:
            self.turn += 360

        # Change the square
        x[self.i, self.j] = write_color
        # This physically(??) moves the turmite
        dirs[self.turn]()

        # Bounds checking, wraps when OoB
        dim = x.shape
        if self.i > (dim[0] - 1):
            self.i -= dim[0]
        elif self.i < 0:
            self.i += dim[0]
        if self.j > (dim[1] - 1):
            self.j -= dim[1]
        elif self.j < 0:
            self.j += dim[1]

        self.state = next_state
        self.color = x[self.i, self.j]
        x[self.i, self.j] = 2
        return x


# Started with a given set, gradHwy, then started changing things til I got interesting ones
# Define rules                    State 0                 State 1                   State 2
options = {'gradHwy':   [[(1, 2, 1), (1, 2, 0)], [(0, 2, 0), (1, 1, 1)]],
           'plusSign':  [[(1, 8, 2), (0, 1, 0)], [(1, 8, 0), (0, 1, 0)], [(1, 8, 1), (0, 8, 1)]],
           'lines':     [[(1, 8, 2), (0, 1, 1)], [(1, 8, 0), (0, 1, 0)], [(1, 8, 1), (0, 8, 1)]],  # draw lines,get stuk
           'miner':     [[(1, 4, 2), (0, 1, 0)], [(1, 8, 0), (0, 2, 0)], [(1, 8, 1), (0, 8, 1)]],  # f'n cool, try it!
           # Note about miner: if you stare into its 'mound' and look away, everything is trippy for a bit
           'harry':     [[(1, 2, 2), (0, 1, 0)], [(1, 8, 0), (0, 2, 0)], [(1, 8, 1), (0, 4, 1)]],
           'quk45Hwy':  [[(1, 2, 2), (0, 1, 0)], [(1, 8, 0), (0, 2, 0)], [(0, 8, 1), (1, 4, 1)]],
           'hwyGoNow':  [[(1, 2, 2), (0, 1, 0)], [(0, 2, 0), (0, 2, 0)], [(0, 8, 1), (1, 4, 1)]],
           'lines':     [[(1, 2, 1), (0, 1, 0)], [(1, 2, 2), (0, 2, 0)], [(0, 8, 1), (1, 4, 1)]],
           'weave':      [[(1, 2, 1), (0, 1, 0)], [(1, 8, 2), (0, 2, 1)], [(0, 8, 1), (1, 4, 1)]],
           'aLine':      [[(1, 8, 1), (1, 0, 1)], [(1, 8, 2), (0, 2, 1)], [(0, 8, 0), (1, 4, 1)]],
           'flline':      [[(1, 8, 1), (1, 0, 1)], [(1, 8, 2), (0, 8, 1)], [(1, 4, 1), (1, 4, 0)]],
           'cross':      [[(1, 4, 1), (1, 4, 1)], [(1, 8, 2), (0, 8, 1)], [(1, 4, 1), (1, 4, 0)]],
           'test':      [[(0, 4, 0), (1, 8, 1)], [(0, 8, 1), (1, 1, 2)], [(1, 4, 2), (0, 8, 0)]]
           }

# Create empty grid
shape = (250, 250)
X = np.zeros(shape, int)

# Create turmite with given rules
rules = np.array(options['miner'])
init_loc = (120, 154)
T = Turmite(init_loc, X, rules)

img = plt.imshow(X, cmap='copper', interpolation='nearest', animated=True)
plt.title("Turmites Oh No")
plt.tight_layout()


# File I/O !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def update_mound(*args):
    global cycles, start
    img.set_array(T.move(X))
    cycles += 1
    if cycles % 100 == 0:
        end = time.perf_counter()
        # print(100 / (end - start))
        print(cycles)
        start = time.perf_counter()
    return img,

cycles = 0
start = time.perf_counter()
vis = animation.FuncAnimation(fig, update_mound, interval=0, blit=True,)

plt.savefig('tur.png')
pylab.show()

