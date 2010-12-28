import math
from random import random
import pygame

from vector import Vector

class Map(object):
    def __init__(self, mimage, wimage, duplication=(1,1), position=None, ships=[], wind_direction = 0, windspeed=0, screensize=(1024,768)):
        self.tile = pygame.image.load(mimage)
        self.wind = pygame.image.load(wimage)
        #self.position = position    # where is the center of the screen?
        self.surface = pygame.Surface((self.tile.get_width()*duplication[0],
                                      self.tile.get_height()*duplication[1]))
        self.wind_direction = wind_direction
        self.windspeed = windspeed
        # Init the map background
        for x in range(duplication[0]):
            for y in range(duplication[1]):
                self.surface.blit(self.tile, (x*self.tile.get_width(),
                                              y*self.tile.get_height()))
        self.ships = ships
        if position is None:
            self.position = Vector(self.surface.get_width(),
                                    self.surface.get_height())/2
        else:
            self.position = position

        self.screensize=screensize


    def get_visible_rect(self):
        return pygame.Rect(self.position.x-self.screensize[0]//2,
                           self.position.y-self.screensize[1]//2,
                           self.screensize[0], self.screensize[1])

    def get_visible_surface(self):
        return self.surface.subsurface(self.get_visible_rect())

    def get_screen_coords(self, mapcoords):
        return (mapcoords-self.position+Vector(self.screensize[0]//2,self.screensize[1]//2))


    def get_wind_vector(self):
        return self.windspeed*Vector(math.cos(self.wind_direction), -math.sin(self.wind_direction))

    def get_windsurface(self, scale=1):
        #scale and transform windarrow
        return (pygame.transform.rotozoom(self.wind, (math.degrees(self.wind_direction)), scale))

    def change_wind(self):
        new_wind = random()-0.5
        self.wind_direction += new_wind
        return self.wind_direction
