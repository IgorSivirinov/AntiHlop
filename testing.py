from typing import List
from Wall import Wall
import matplotlib.animation as animation
import matplotlib.pyplot as plt
ani_obj, = plt.plot([], [], '-', color='r',
                         lw=1,
                         label='Ball')
print(type(ani_obj))