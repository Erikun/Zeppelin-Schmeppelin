#from __future__ import division

from math import *

class Vector(object):
    def __init__(self, x, y=0):
        if type(x).__name__ == "tuple":
            self.x, self.y = x
        else:
            self.x, self.y = x, y

    def __index__(self, n):
        if n == 0:
            return self.x
        elif n == 1:
            return self.y

    def norm(self):
        return sqrt(self.x**2 + self.y**2)

    def __mul__(self, t):
        return Vector(t*self.x, t*self.y)

    def __rmul__(self, t):
        return self*t

    def __truediv__(self, t):   # must be named this to work with future-division
        return Vector(self.x/t, self.y/t)

    def __div__(self, t):
        return Vector(self.x/t, self.y/t)

    def __rdiv__(self, t):
        return Vector(self.x/t, self.y/t)

    def normalized(self):
        return self/self.norm()
        #self.norm()

    def __add__(self, v):
        return Vector(self.x+v.x, self.y+v.y)

    def __sub__(self, v):
        return Vector(self.x-v.x, self.y-v.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __repr__(self):
        return "(%f, %f)"%(self.x, self.y)

    def scalar(self, v):
        return self.x*v.x + self.y*v.y

    def rotate(self, theta):
        xp = self.x*cos(theta) - self.y*sin(theta)
        yp = self.y*cos(theta) + self.x*sin(theta)

        return Vector(xp, yp)

    def tuple(self):
        return (self.x, self.y)

