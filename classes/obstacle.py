

class Obstacle:
    def __init__(self, nom, img, x, y, h, l):
        self.nom = nom
        self.img = img
        self.x = x
        self.y = y
        self.h = h
        self.l = l
    
    def print(self):
        print("obstacle x=", self.x, "y=", self.y, "l=", self.l, "h=", self.h)