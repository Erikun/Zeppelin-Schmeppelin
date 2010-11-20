from __future__ import division

import pygame, time, math
from pygame.locals import *
from pygame import gfxdraw
from vector import Vector
from random import random


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
    def __init__(self, image, shadowimage, position=Vector(0,0), heading=0, speed=30, rotation=0):
        self.image = pygame.image.load(image)
        self.shadowimage = pygame.image.load(shadowimage)
        self.position = position
        self.heading = heading
        self.speed = speed
        self.rotation = rotation

    def get_surface(self):
        return (pygame.transform.rotozoom(self.image, math.degrees(self.heading), SCALE),
                pygame.transform.rotozoom(self.shadowimage, math.degrees(self.heading), SCALE))


    def get_direction_vector(self):
        return Vector(math.cos(self.heading),
                      -math.sin(self.heading))

    def update(self, t):
        self.speed += self.acceleration*t

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
    def __init__(self, image, position=Vector(0,0)):
        self.tile = pygame.image.load(image)
        self.position = position
        self.surface = pygame.Surface((self.tile.get_width()*5,
                                      self.tile.get_height()*5))
        self.position = Vector((self.tile.get_width()*5,
                                self.tile.get_height()*5))/2
        for x in range(5):
            for y in range(5):
                print self.surface.blit(self.tile, (x*self.tile.get_width(),
                                              y*self.tile.get_height()))



airship = Airship('airship.png', 'shadow.png')
map = Map("forest.png")

def draw_background(map):
    screen.blit(map.surface, (0,0),
                pygame.Rect(map.position.x - SWIDTH//2, map.position.y-SHEIGHT//2,
                            SWIDTH, SHEIGHT))

def draw_all(screen, ships, blips):
    # draw everything
    #screen.fill(GREEN)
    draw_background(map)

    for ship in ships:
        #airship.angle += 1
        airship_surf = ship.get_surface()
        img_size = Vector(airship_surf[0].get_width()//2, airship_surf[0].get_height()//2)
        screen.blit(airship_surf[1], (mapcenter+airship.position-img_size+Vector(20,20)).tuple())
        screen.blit(airship_surf[0], (mapcenter+airship.position-img_size).tuple())

        for i, b in enumerate(blips):
            blip_pos = (mapcenter+b)
            gfxdraw.filled_circle(screen, blip_pos.x, blip_pos.y, 3, (255,0,0))

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
        mousedir = mousepos - airship.position - mapcenter
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
                         (mapcenter+airship.position).tuple(),
                         (mapcenter+airship.position+mousedir/mousedist*airship.speed).tuple(),
                         7)
        pygame.draw.line(screen, (255,0,0),
                         (mapcenter+airship.position).tuple(),
                         mousepos.tuple(), 3)

        pygame.display.flip()

    airship.set_rotation( mouseangle )
    airship.acceleration = max(-10, min(10, (mousedist-airship.speed)/20))
    print airship.acceleration, airship.rotation


    # And here is the "realtime" part

    blips = []
    orig_pos = airship.position
    for i,t in enumerate(xrange(FRAMES_PER_SECOND*TURNTIME)):   # 100 ticks == 3 s
        airship.update(1./FRAMES_PER_SECOND*TURNTIME)

        # let's move the ship
        airship.move(1./(FRAMES_PER_SECOND*TURNTIME))
        airship.turn(1./(FRAMES_PER_SECOND*TURNTIME))

        if i%10 == 0:
            blips.append(airship.position)

        clock.tick(FRAMES_PER_SECOND)
        draw_all(screen, [airship], blips)

    delta_pos = airship.position - orig_pos

