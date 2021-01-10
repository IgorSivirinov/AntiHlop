from Wall import Wall
class Room:
    walls:list = []
    def __init__(self, wall_1:Wall, wall_2:Wall):
        self.walls.append(wall_1)
        self.walls.append(wall_2)
