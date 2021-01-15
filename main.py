import constants
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from typing import List
from Wall import Wall
from Sound_Wave import Sound_Wave

def get_volume(R,time, E):
    S = 4*np.pi*R**2

    intensity_sound = E/(time*S)

    volume = np.log10(intensity_sound/constants.I0)*10

    if volume<0:
        volume = 0

    return volume

def start_anim(occurrence_rate, width, height, sound_volume, x, y, walls:List[Wall]):

    E = 10**(sound_volume/10)*constants.I0*4*np.pi*(1/335)

    fig, ax = plt.subplots()

    plt.axis('equal')

    ax.set_xlim( 0, width)
    ax.set_ylim(-3, height)

    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    for i in walls:
        plt.plot(i.get_creation_coordinates()[0], i.get_creation_coordinates()[1], '-', color='k', lw=5)

    def animate(i):
        wave = Sound_Wave(x,y,[],get_volume(((i*0.1)/occurrence_rate) * 335,(i*0.1)/occurrence_rate, E))
        time_text.set_text(str(get_volume(i*0.1/occurrence_rate * 335,i*0.1/occurrence_rate, E)) +' дБ \n'+
                           str(int((i*0.1/occurrence_rate)*1000)) +' мс')
        wave.move(walls,occurrence_rate,i)

    ani = animation.FuncAnimation(fig, animate, frames=range(1,20), interval=500)
    plt.show()
    # ani.save('AntiHlop_Test004.gif')


walls = [Wall(3,3,4,0.7,0.3,Wall.Location.vertically)]
start_anim(50,13,10,40,5,1,walls)