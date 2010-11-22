from __future__ import division

import pygame, time, math
from pygame.locals import *
from pygame import gfxdraw, Rect
from vector import Vector
from random import random

pygame.init()

SWIDTH, SHEIGHT = 1024, 768
screen = pygame.display.set_mode((SWIDTH, SHEIGHT), DOUBLEBUF)

GREEN = (20,150,20)
MAP_CENTER = Vector(SWIDTH//2, SHEIGHT//2)
SCALE = 0.25

clock = pygame.time.Clock()
FRAMES_PER_SECOND = 30
TURNTIME = 3  # s

class Airship(object):
    """
    A class to describe an airship
    """
    def __init__(self, image, shadowimage, position=Vector(0,0), heading=0, speed=30, acceleration=0, rotation=0):
        self.image = pygame.image.load(image)
        self.shadowimage = pygame.image.load(shadowimage)
        self.position = position
        self.heading = heading
        self.speed = speed
        self.acceleration = acceleration
        self.rotation = rotation
        self.max_speed_forwards = 100
        self.max_speed_backwards = -50


    def get_surface(self):
        return (pygame.transform.rotozoom(self.image, math.degrees(self.heading), SCALE),
                pygame.transform.rotozoom(self.shadowimage, math.degrees(self.heading), SCALE))

#    def get_surface_size(self):
#        return Vector(self.image.get_width(), self.image.get_height())


    def get_direction_vector(self):
        return Vector(math.cos(self.heading),
                      -math.sin(self.heading))

    def update(self, t):
        self.speed = max(self.max_speed_backwards,
                         min(self.max_speed_forwards, self.speed+self.acceleration*t))

    def move(self, t):
        direction = self.get_direction_vector()
        self.position = self.position + direction*self.speed*t

    def turn(self, t):
        self.heading += self.rotation*t

    def get_position_tuple(self):
        return (self.position.x, self.position.y)

    def set_rotation(self, newrotation):
        self.rotation = max(math.radians(-25), min(newrotation, math.radians(25)))

class Map(object):
    def __init__(self, image, position=None, ships=[]):
        self.tile = pygame.image.load(image)
        #self.position = position    # where is the center of the screen?
        self.surface = pygame.Surface((self.tile.get_width()*5,
                                      self.tile.get_height()*5))
        # Init the map background
        for x in range(5):
            for y in range(5):
                self.surface.blit(self.tile, (x*self.tile.get_width(),
                                              y*self.tile.get_height()))
        self.ships = ships
        if position is None:
            self.position = Vector(self.surface.get_width(),
                                    self.surface.get_height())/2
        else:
            self.position = position


    def get_visible_rect(self):
        return pygame.Rect(self.position.x-SWIDTH//2,
                           self.position.y-SHEIGHT//2,
                           SWIDTH, SHEIGHT)

    def get_visible_surface(self):
        return self.surface.subsurface(self.get_visible_rect())

    def get_screen_coords(self, mapcoords):
        return (mapcoords-self.position+Vector(SWIDTH//2,SHEIGHT//2))

map = Map("forest.png")
airship = Airship('airship.png', 'shadow.png', position=map.position)


def draw_background(map):
    screen.blit(map.get_visible_surface(), dest=(0,0))

font = pygame.font.Font(None, 36)

def draw_all(screen, ships, blips):
    # draw everything
    #screen.fill(GREEN)
    draw_background(map)

    for ship in ships:
        #airship.angle += 1
        airship_surf = ship.get_surface()
        #img_size = airship.get_surface_size()
        img_size = Vector(airship_surf[0].get_width(),
                          airship_surf[0].get_height())
        print img_size
        print "map_coords:", map.get_screen_coords(airship.position)
        screen.blit(airship_surf[1], (map.get_screen_coords(airship.position)-img_size/2+Vector(20,20)).tuple())
        screen.blit(airship_surf[0], (map.get_screen_coords(airship.position)-img_size/2).tuple())

        for i, b in enumerate(blips):
            blip_pos = (mapcenter+b)
            gfxdraw.filled_circle(screen, blip_pos.x, blip_pos.y, 3, (255,0,0))

        text = font.render("Speed: %.2f Acc:%.2f Turn:%.2f Pos: (%d,%d)"%(ship.speed, ship.acceleration, math.degrees(ship.rotation), ship.position.x, ship.position.y), 1, (255,255,255))

        screen.blit(text, (5,5))

        pygame.display.flip()
        #print airship_rot.

blips = []
mapcenter = MAP_CENTER
delta_pos = Vector(0,0)

while 1:
    # print "Input your desired speed [0..10]:",
    # airship.speed = input()
    # print "Input your desired turn [-5..5]:",
    # airship.rotation = input()

    # Scroll to center the airship
    # for i in xrange(20):
    #     clock.tick(FRAMES_PER_SECOND)
    #     #draw_all(screen, [airship], blips)
    #     #mapcenter = mapcenter - delta_pos/20
    #     screen.scroll((-delta_pos/20).x, (-delta_pos/20).y)
    #     pygame.display.flip()
    # mapcenter -= delta_pos


    # This is the user input loop
    clicked = False
    while not clicked:
        clock.tick(FRAMES_PER_SECOND)
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                clicked = True

        mousepos = Vector(pygame.mouse.get_pos())
        #print mousepos
        airship_screenpos = map.get_screen_coords(airship.position)
        mousedir = mousepos - airship_screenpos
        mousedist = math.sqrt(mousedir.x**2 + mousedir.y**2)
        mouseangle = math.acos(mousedir.x/mousedist)
        if mousedir.y > 0:
            mouseangle = math.pi*2 - mouseangle

        mouseangle -= airship.heading
        if mouseangle > math.pi:
            mouseangle = -math.pi*2 + mouseangle
        elif mouseangle < -math.pi:
            mouseangle = math.pi*2 + mouseangle

        print mousedist , mouseangle
        draw_all(screen, [airship], blips)
        pygame.draw.line(screen, (0,100,255),
                         airship_screenpos.tuple(),
                         (airship_screenpos+mousedir/mousedist*airship.speed).tuple(),
                         7)
        pygame.draw.line(screen, (255,0,0),
                         airship_screenpos.tuple(),
                         mousepos.tuple(), 3)

        pygame.display.flip()

    airship.set_rotation( mouseangle )
    airship.acceleration = max(-10, min(10, (mousedist-airship.speed)/20))
    print airship.acceleration, airship.rotation


    # And here is the "realtime" part

    blips = []
    orig_pos = airship.position
    #for i,t in enumerate(xrange(FRAMES_PER_SECOND*TURNTIME)):   # 100 ticks == 3 s
    i=t=0
    clicked = False
    while not clicked:
        airship.update(1./FRAMES_PER_SECOND*TURNTIME)

        # let's move the ship
        airship.move(1./(FRAMES_PER_SECOND*TURNTIME))
        airship.turn(1./(FRAMES_PER_SECOND*TURNTIME))

        if i%30 == 0:
            blips.append(airship.position)

        clock.tick(FRAMES_PER_SECOND)
        draw_all(screen, [airship], blips)

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                clicked = True
        #map.position += Vector(0,1)

        ship_screen_pos = airship.position - map.position
        print "ship_screen_pos:", ship_screen_pos
        d = 0.3
        if ship_screen_pos.x > SWIDTH * d:
            map.position += ship_screen_pos - Vector(SWIDTH*d, ship_screen_pos.y)
        if ship_screen_pos.x < -(SWIDTH * d):
            map.position -= ship_screen_pos + Vector(SWIDTH*d, ship_screen_pos.y)
        if ship_screen_pos.y > SHEIGHT * d:
            map.position += ship_screen_pos - Vector(ship_screen_pos.x, SHEIGHT*d)
        if ship_screen_pos.x < -(SHEIGHT * d):
            map.position -= ship_screen_pos + Vector(ship_screen_pos.x, SHEIGHT*d)

        i += 1
        t += 1/FRAMES_PER_SECOND

    delta_pos = airship.position - orig_pos

