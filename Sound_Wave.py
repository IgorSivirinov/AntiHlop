import constants
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sympy as sy
import math
from typing import List
from Wall import Wall
from enum import Enum

class Sound_Wave:

    ani_obj:matplotlib.lines.Line2D

    x:float
    y:float

    class Drawing(Enum):
        left = 0
        right = 1
        up = 2
        down = 3
        no = 4

    drawing: Drawing

    mas_bring_walls:List[Wall]

    start_valume:float

    def __init__(self, x, y, mas_bring_walls, volume, drawing:Drawing = Drawing.no):

        self.x = x
        self.y = y
        self.mas_bring_walls = mas_bring_walls
        self.start_valume = volume
        self.ani_obj, = plt.plot([], [], '-', color='r',
                         lw=volume / 10,
                         label='Ball')
        self.drawing = drawing

        if (x<= 0 and y <= 0):
            raise Exception("Creation coordinates x and y cannot be less than zero")
        elif (x <= 0):
            raise Exception("Creation coordinate x cannot be less than zero")
        elif (y <= 0):
            raise Exception("Creation coordinate y cannot be less than zero")

    def move(self, walls, occurrence_rate, time):
        self.ani_obj.set_data(self.__move__(walls,occurrence_rate,time))

    def __move__(self, walls, occurrence_rate, time):

        R = ((time * 0.1) / occurrence_rate) * 335

        alpha = np.arange(0, 2 * np.pi, 0.01)

        x = R * np.cos(alpha) + self.x
        y = R * np.sin(alpha) + self.y

        for a in range(len(y)):

            if (self.drawing == Sound_Wave.Drawing.up and y[a]<self.y):
                y[a] = self.y
            elif (self.drawing == Sound_Wave.Drawing.down and y[a]>self.y):
                y[a] = self.y
            elif (self.drawing == Sound_Wave.Drawing.left and x[a] > self.x):
                x[a] = self.x
            elif (self.drawing == Sound_Wave.Drawing.right and x[a]<self.x):
                x[a] = self.x

            for wall in walls:
                # x = y/k - b
                # k = tg(alpha)
                if ((y[a] > wall.y and wall.type == Wall.Location.horizontally and self.y < wall.y)):

                    k1 = sy.Abs(self.y - wall.get_creation_coordinates()[1][0]) / sy.Abs(
                        self.x - wall.get_creation_coordinates()[0][0])
                    k2 = sy.Abs(self.y - wall.get_creation_coordinates()[1][1]) / sy.Abs(
                        self.x - wall.get_creation_coordinates()[0][1])

                    if (self.x > wall.get_creation_coordinates()[0][1]):
                        k1 *= -1
                        k2 *= -1
                    elif(self.x > wall.get_creation_coordinates()[0][0] and self.x < wall.get_creation_coordinates()[0][1]):
                        k1 *= -1


                    x01 = (wall.get_creation_coordinates()[1][0] / k1 - wall.get_creation_coordinates()[0][0]) * -1
                    x02 = (wall.get_creation_coordinates()[1][1] / k2 - wall.get_creation_coordinates()[0][1]) * -1

                    if (x[a] > (y[a] / k1 + x01) and x[a] < (y[a] / k2 + x02)):

                        if (x[a] < ((y[a] / k1 + x01) + (((y[a] / k2 + x02)) - (y[a] / k1 + x01)) / 2)):
                            x[a] = wall.get_creation_coordinates()[0][0]
                        else:
                            x[a] = wall.get_creation_coordinates()[0][1]

                        y[a] = wall.y
                        mas_walls_belongs:List[Wall] = []

                        for wall_c in walls:
                            if (wall_c.chek_belongs_point(self.x, self.y)):
                                mas_walls_belongs.append(wall_c)
                        if(mas_walls_belongs.count(wall)==0 and not wall.chek_celongs_wall(self)):

                            new_x:float

                            if(self.x<wall.get_creation_coordinates()[0][0]):
                                new_x =  wall.get_creation_coordinates()[0][0]
                            elif (self.x > wall.get_creation_coordinates()[0][1]):
                                new_x =  wall.get_creation_coordinates()[0][1]
                            else:
                                new_x = self.x

                            new_wave1 = Sound_Wave(new_x, wall.y
                                                    ,[]
                                                    ,self.start_valume * wall.reflection_index
                                                    ,Sound_Wave.Drawing.down)
                            new_wave1.move(walls, occurrence_rate,
                                           time - ((((wall.y - self.y)**2 + sy.Abs(new_x-self.x)**2)**0.5 / 335) * occurrence_rate * 10))

                            new_wave2 = Sound_Wave(new_x, wall.y
                                                   ,[]
                                                   ,self.start_valume * wall.entry_index
                                                   , Sound_Wave.Drawing.up)
                            new_wave2.move(walls, occurrence_rate,
                                           time - ((((wall.y - self.y)**2 + sy.Abs(new_x-self.x)**2)**0.5 / 335) * occurrence_rate * 10))

                elif ((y[a] < wall.y and wall.type == Wall.Location.horizontally and self.y > wall.y)):

                    k1 = sy.Abs(wall.get_creation_coordinates()[1][0] - self.y ) / sy.Abs(
                        self.x - wall.get_creation_coordinates()[0][0])
                    k2 = sy.Abs(wall.get_creation_coordinates()[1][1] - self.y ) / sy.Abs(
                        self.x - wall.get_creation_coordinates()[0][1])

                    k1 *= -1
                    k2 *= -1
                    if (self.x > wall.get_creation_coordinates()[0][1]):
                        k1 *= -1
                        k2 *= -1
                    elif (self.x > wall.get_creation_coordinates()[0][0] and self.x <
                          wall.get_creation_coordinates()[0][1]):
                        k1 *= -1

                    x01 = (wall.get_creation_coordinates()[1][0] / k1 - wall.get_creation_coordinates()[0][0]) * -1
                    x02 = (wall.get_creation_coordinates()[1][1] / k2 - wall.get_creation_coordinates()[0][1]) * -1

                    wave_wall_1: float = self.x
                    wave_wall_2: float = self.x
                    if (k1 != 0):
                        x01 = (wall.get_creation_coordinates()[1][0] / k1 - wall.get_creation_coordinates()[0][0]) * -1
                        wave_wall_1 = y[a] / k1 + x01
                    if (k2 != 0):
                        x02 = (wall.get_creation_coordinates()[1][1] / k2 - wall.get_creation_coordinates()[0][1]) * -1
                        wave_wall_2 = k2*(x[a]-x02)

                    if (y[a] >  wave_wall_1 and y[a] <  wave_wall_2):

                        if (y[a] < (wave_wall_1) + (wave_wall_2 - wave_wall_1) / 2):
                    if (x[a] > (y[a] / k1 + x01) and x[a] < (y[a] / k2 + x02)):
                        if (x[a] < ((y[a] / k1 + x01) + (((y[a] / k2 + x02)) - (y[a] / k1 + x01)) / 2)):
                            x[a] = wall.get_creation_coordinates()[0][0]
                        else:
                            x[a] = wall.get_creation_coordinates()[0][1]

                        y[a] = wall.y
                        mas_walls_belongs: List[Wall] = []

                        for wall_c in walls:
                            if (wall_c.chek_belongs_point(self.x, self.y)):
                                mas_walls_belongs.append(wall_c)
                        if (mas_walls_belongs.count(wall) == 0 and not wall.chek_celongs_wall(self)):

                            new_x: float

                            if (self.x < wall.get_creation_coordinates()[0][0]):
                                new_x = wall.get_creation_coordinates()[0][0]
                            elif (self.x > wall.get_creation_coordinates()[0][1]):
                                new_x = wall.get_creation_coordinates()[0][1]
                            else:
                                new_x = self.x

                            new_wave1 = Sound_Wave(new_x, wall.y
                                                   , []
                                                   , self.start_valume * wall.reflection_index
                                                   , Sound_Wave.Drawing.up)
                            new_wave1.move(walls, occurrence_rate,
                                           time - ((((self.y - wall.y)**2 + sy.Abs(new_x-self.x)**2)**0.5 / 335) * occurrence_rate * 10))

                            new_wave2 = Sound_Wave(new_x, wall.y
                                                   , []
                                                   , self.start_valume * wall.entry_index
                                                   , Sound_Wave.Drawing.down)
                            new_wave2.move(walls, occurrence_rate,
                                           time - ((((self.y - wall.y)**2 + sy.Abs(new_x-self.x)**2)**0.5/ 335) * occurrence_rate * 10))
                elif ((x[a] < wall.x and wall.type == Wall.Location.vertically and self.x > wall.x)):
                    print(sy.Abs(self.y - wall.get_creation_coordinates()[1][0]),"/",
                          sy.Abs(self.x - wall.get_creation_coordinates()[0][0]))
                    k1 = sy.Abs(self.y - wall.get_creation_coordinates()[1][0]) / sy.Abs(self.x - wall.get_creation_coordinates()[0][0])

                    k2 = sy.Abs(self.y - wall.get_creation_coordinates()[1][1]) / sy.Abs(self.x - wall.get_creation_coordinates()[0][1])

                    if (self.y <= wall.get_creation_coordinates()[1][0]):
                        k1 *= -1
                        k2 *= -1
                    elif (self.y > wall.get_creation_coordinates()[1][0] and self.y <
                          wall.get_creation_coordinates()[1][1]):
                        k2 *= -1

                    wave_wall_1: float = self.y
                    wave_wall_2: float = self.y
                    if (k1 != 0):
                        x01 = (wall.get_creation_coordinates()[1][0] / k1 - wall.get_creation_coordinates()[0][0]) * -1
                        wave_wall_1 = k1*(x[a]-x01)
                    if (k2 != 0):
                        x02 = (wall.get_creation_coordinates()[1][1] / k2 - wall.get_creation_coordinates()[0][1]) * -1
                        wave_wall_2 = k2*(x[a]-x02)

                    if (y[a] >  wave_wall_1 and y[a] <  wave_wall_2):

                        if (y[a] < (wave_wall_1) + (wave_wall_2 - wave_wall_1) / 2):
                            y[a] = wall.get_creation_coordinates()[1][0]
                        else:
                            y[a] = wall.get_creation_coordinates()[1][1]

                        x[a] = wall.x

                        if (wall.waves.count(self) == 0):
                            wall.waves.append(self)

                            new_y: float

                            if (self.y < wall.get_creation_coordinates()[1][0]):
                                new_y = wall.get_creation_coordinates()[1][0]
                            elif (self.y > wall.get_creation_coordinates()[1][1]):
                                new_y = wall.get_creation_coordinates()[1][1]
                            else:
                                new_y = self.y

                            new_wave1 = Sound_Wave(wall.x, new_y
                                                   , []
                                                   , self.start_valume * wall.reflection_index
                                                   , Sound_Wave.Drawing.right)
                            new_wave1.move(walls, occurrence_rate,
                                           time - ((((self.y - new_y) ** 2 + sy.Abs(
                                               self.x - wall.x) ** 2) ** 0.5 / 335) * occurrence_rate * 10))

                            new_wave2 = Sound_Wave(wall.x, new_y
                                                   , []
                                                   , self.start_valume * wall.entry_index
                                                   , Sound_Wave.Drawing.left)
                            new_wave2.move(walls, occurrence_rate,
                                           time - ((((self.y - new_y) ** 2 + sy.Abs(
                                               self.x - wall.x) ** 2) ** 0.5 / 335) * occurrence_rate * 10))

                elif ((x[a] > wall.x and wall.type == Wall.Location.vertically and self.x < wall.x)):
                    k1 = sy.Abs(self.y - wall.get_creation_coordinates()[1][0]) / sy.Abs(
                        self.x - wall.get_creation_coordinates()[0][0])

                    k2 = sy.Abs(self.y - wall.get_creation_coordinates()[1][1]) / sy.Abs(
                        self.x - wall.get_creation_coordinates()[0][1])

                    k1 *= -1
                    k2 *= -1
                    if (self.y < wall.y):
                        k1 *= -1
                        k2 *= -1

                    x01 = (wall.get_creation_coordinates()[1][0] / k1 - wall.get_creation_coordinates()[0][0]) * -1
                    x02 = (wall.get_creation_coordinates()[1][1] / k2 - wall.get_creation_coordinates()[0][1]) * -1

                    print(y[a], ":", x[a])
                    print(k1 * (x[a] - x01), "-", k2 * (x[a] - x02))
                    if (y[a] > k1 * (x[a] - x01) and y[a] < k2 * (x[a] - x02)):

                        if (y[a] < ((k1 * (x[a] - x01)) + ((k2 * (x[a] - x02)) - (k1 * (x[a] - x01))) / 2)):
                            y[a] = wall.get_creation_coordinates()[1][0]
                        else:
                            y[a] = wall.get_creation_coordinates()[1][1]

                        x[a] = wall.x

                        if (wall.waves.count(self) == 0):
                            wall.waves.append(self)

                            new_y: float

                            if (self.y < wall.get_creation_coordinates()[1][0]):
                                new_y = wall.get_creation_coordinates()[1][0]
                            elif (self.y > wall.get_creation_coordinates()[1][1]):
                                new_y = wall.get_creation_coordinates()[1][1]
                            else:
                                new_y = self.y

                            new_wave1 = Sound_Wave(wall.x, new_y
                                                   , []
                                                   , self.start_valume * wall.reflection_index
                                                   , Sound_Wave.Drawing.right)
                            new_wave1.move(walls, occurrence_rate,
                                           time - ((((self.y - new_y) ** 2 + sy.Abs(
                                               self.x - wall.x) ** 2) ** 0.5 / 335) * occurrence_rate * 10))

                            new_wave2 = Sound_Wave(wall.x, new_y
                                                   , []
                                                   , self.start_valume * wall.entry_index
                                                   , Sound_Wave.Drawing.left)
                            new_wave2.move(walls, occurrence_rate,
                                           time - ((((self.y - new_y) ** 2 + sy.Abs(
                                               self.x - wall.x) ** 2) ** 0.5 / 335) * occurrence_rate * 10))

                    #     if (vx0 != room.walls[1].length):
                    #         ball, = plt.plot([], [], '-', color='r',lw=sound_volume / 10)
                    #         ball.set_data(circle_move(room.walls[1].length, vy0,
                    #                                   sound_volume,
                    #                                   time - (((room.walls[1].length-vx0)/335)*occurrence_rate*10)))
                    # # if(vy0!=room.walls[0].length and not y2):
                    #     ball, = plt.plot([], [], '-', color='r',lw=sound_volume / 10)
                    #     ball.set_data(circle_move(vx0, room.walls[0].length,
                    #                               sound_volume,
                    #                               time - (((room.walls[0].length - vy0)/335)*occurrence_rate*10)))
                    #     y2 = True

                # if(y[a]<0):
                #     y[a]=0
                # if(vy0!=0 and not y1):
                #     ball, = plt.plot([], [], '-', color='r', lw=sound_volume/ 10)
                #     ball.set_data(circle_move(vx0, 0,
                #                               sound_volume,
                #                               time - ((vy0/335)*occurrence_rate*10)))
                #     y1 = True

                # if(x[a]>room.walls[1].length):
                #     x[a]=room.walls[1].length
                # if(vx0!=room.walls[1].length and not x2):
                #     ball, = plt.plot([], [], '-', color='r',lw=sound_volume / 10)
                #     ball.set_data(circle_move(room.walls[1].length, vy0,
                #                               sound_volume,
                #                               time - (((room.walls[1].length-vx0)/335)*occurrence_rate*10)))
                #     x2 = True

                # if(x[a]<0):
                #     x[a]=0
                # if(vx0!=0 and not x1):
                #     ball, = plt.plot([], [], '-', color='r',lw=sound_volume / 10)
                #     ball.set_data(circle_move(0, vy0,
                #                               sound_volume,
                #                               time - ((vx0/335)*occurrence_rate*10)))
                #     x1 = True

        return x, y

    def comparison(self, obj):
        return (self.x == obj.x and
                self.y == obj.y and
                self.mas_bring_walls == obj.mas_bring_walls)




