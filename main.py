import constants
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from Room import Room
from Wall import Wall
def get_volume(R,time, E):
    S = 4*np.pi*R**2

    intensity_sound = E/(time*S)

    volume = np.log10(intensity_sound/constants.I0)*10

    if volume<0:
        volume = 0

    return volume
def start_anim(occurrence_rate, sound_volume, x, y, room:Room):
    E = 10**(sound_volume/10)*constants.I0*4*np.pi*(1/335)

    fig, ax = plt.subplots()

    plt.axis('equal')

    ax.set_xlim(0, room.walls[1].length)
    ax.set_ylim(0, room.walls[0].length)

    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


    def circle_move(vx0, vy0, sound_volume, time):

        R = ((time*0.1)/occurrence_rate) * 335

        alpha = np.arange(0, 2 * np.pi, 0.1)

        x = R * np.cos(alpha) + vx0
        y = R * np.sin(alpha) + vy0

        y1 = False
        y2 = False
        x1 = False
        x2 = False

        for a in range(len(y)):

            if(y[a]>room.walls[0].length):
                y[a]=room.walls[0].length
                if(vy0!=room.walls[0].length and not y2):
                    ball, = plt.plot([], [], '-', color='r',lw=sound_volume / 10)
                    ball.set_data(circle_move(vx0, room.walls[0].length,
                                              sound_volume,
                                              time - (((room.walls[0].length - vy0)/335)*occurrence_rate*10)))
                    y2 = True

            if(y[a]<0):
                y[a]=0
                if(vy0!=0 and not y1):
                    ball, = plt.plot([], [], '-', color='r', lw=sound_volume/ 10)
                    ball.set_data(circle_move(vx0, 0,
                                              sound_volume,
                                              time - ((vy0/335)*occurrence_rate*10)))
                    y1 = True

            if(x[a]>room.walls[1].length):
                x[a]=room.walls[1].length
                if(vx0!=room.walls[1].length and not x2):
                    ball, = plt.plot([], [], '-', color='r',lw=sound_volume / 10)
                    ball.set_data(circle_move(room.walls[1].length, vy0,
                                              sound_volume,
                                              time - (((room.walls[1].length-vx0)/335)*occurrence_rate*10)))
                    x2 = True

            if(x[a]<0):
                x[a]=0
                if(vx0!=0 and not x1):
                    ball, = plt.plot([], [], '-', color='r',lw=sound_volume / 10)
                    ball.set_data(circle_move(0, vy0,
                                              sound_volume,
                                              time - ((vx0/335)*occurrence_rate*10)))
                    x1 = True

        return x, y

    plt.plot([0,0], [0,room.walls[0].length], '-', color='k', lw=3)
    plt.plot([room.walls[1].length, room.walls[1].length], [0, room.walls[0].length], '-', color='k', lw=3)
    plt.plot([0, room.walls[1].length], [room.walls[0].length, room.walls[0].length], '-', color='k', lw=3)
    plt.plot([0, room.walls[1].length], [0, 0], '-', color='k', lw=3)

    def animate(i):
        ball, = plt.plot([], [], '-', color='r', lw=get_volume(((i*0.1)/occurrence_rate) * 335,(i*0.1)/occurrence_rate, E)/10, label='Ball')
        time_text.set_text(str(get_volume(i*0.1/occurrence_rate * 335,i*0.1/occurrence_rate, E)) +' дБ \n'+
                           str((i*0.1/occurrence_rate)*1000) +' мс')
        ball.set_data(circle_move(vx0=x, vy0=y,sound_volume=get_volume(((i*0.1)/occurrence_rate) * 335,(i*0.1)/occurrence_rate, E), time=i))

    ani = animation.FuncAnimation(fig, animate, frames=range(1,50), interval=500)

    ani.save('AntiHlop_Test002.gif')

start_anim(30, 50, 2, 3, Room(Wall(10,2,2), Wall(7,1,1)))
