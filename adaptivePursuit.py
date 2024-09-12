import os
import re
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from scipy.signal import savgol_filter
import sys
import random

fig, ax = plt.subplots()

for i in range(10):
    x = 2*np.cos(i*(2*np.pi)/10)
    y = 2*np.sin(i*(2*np.pi)/10)

    plt.scatter(x,y, s=8)
plt.scatter(0,0, s=8)
ax.set_aspect(1)
plt.show()