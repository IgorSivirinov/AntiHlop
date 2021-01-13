from enum import Enum
from typing import List
class Wall:

    x:float
    y:float

    class Location(Enum):
        horizontally = 0
        vertically = 1
    type: Location


    length:float

    reflection_index:float
    entry_index:float

    waves:list

    def __init__(self,x:float, y:float, length:float, reflection_index:float, entry_index:float, type_loation:Location):

        self.x = x
        self.y = y

        self.length = length

        self.reflection_index = reflection_index
        self.entry_index = entry_index

        self.type = type_loation

        self.waves = []

        if ((x - (length/2) < 0 and Wall.Location.horizontally == type_loation)
                and (y - (length/2) < 0 and Wall.Location.vertically == type_loation)):
            raise Exception("Creation coordinates x and y cannot be less than zero")
        elif (x - (length/2) < 0 and Wall.Location.horizontally == type_loation):
            raise Exception("Creation coordinate x cannot be less than zero")
        elif (y - (length/2) < 0 and Wall.Location.vertically == type_loation):
            raise Exception("Creation coordinate y cannot be less than zero")

    def get_creation_coordinates(self):
        if(self.type == Wall.Location.horizontally):
            X = [self.x - (self.length/2), self.x+(self.length/2)]
            Y = [self.y,self.y]
        else:
            X = [self.x, self.x]
            Y = [self.y - (self.length / 2), self.y + (self.length / 2)]
        return X, Y

    def chek_belongs_point(self,x,y):
        if(self.type == Wall.Location.horizontally):
            return y==self.y and x>=self.get_creation_coordinates()[0][0] and x<=self.get_creation_coordinates()[0][1]
        else:
            return x==self.y and y>=self.get_creation_coordinates()[0][0] and y<=self.get_creation_coordinates()[0][1]

    def chek_celongs_wall(self, wave):
        for belongs_walls in self.waves:
            if(wave.comparison(belongs_walls)):
                return True
        return False


    def comparison(self, obj):
        return (self.x == obj.x and
                self.y == obj.y and
                self.length == obj.length and
                self.type == obj.type and
                self.waves == obj.waves)