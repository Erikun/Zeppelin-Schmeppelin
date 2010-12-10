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

class Order(object):
    """
    An order given to a ship
    """
    def __init__(self, turn=0, motor=-1):
        self.turn = turn
        self.motor = motor


class Airship(object):
    """
    A class to describe an airship
    """
    def __init__(self, image, shadowimage, position=Vector(0,0), heading=0,
                 airspeed=0, acceleration=0, angular_freq=0, motor=0, torque=0):
        self.image = pygame.image.load(image)
        self.shadowimage = pygame.image.load(shadowimage)
        self.position = position
        self.heading = heading       # rad
        self.airspeed = airspeed     # m/s
        #self.acceleration = acceleration
        self.mass = 10000.0   # kg
        self.moment_of_inertia = 1000   # Nms**2
        self.angular_freq = angular_freq   # rad/s
        self.motor_force = motor       # N
        self.torque = torque     # Nm
        self.max_motor_force_forwards = 30000
        self.max_motor_force_backwards = -10000
        #self.max_rotation = 10     # degrees/s
        self.max_torque = 50  # absolute
        self.air_drag = 1000   # Ns/m
        self.turn_drag = 200   #
        self.orders = []

    def get_surface(self):
        """
        Create a surface containing the scaled and rotated ship + shadow
        """
        return (pygame.transform.rotozoom(self.image,
                                          math.degrees(self.heading), SCALE),
                pygame.transform.rotozoom(self.shadowimage,
                                          math.degrees(self.heading), SCALE))

#    def get_surface_size(self):
#        return Vector(self.image.get_width(), self.image.get_height())

    def give_order(self, order):
        if len(self.orders) < 3:
            self.orders.append(order)

    def carry_out_order(self):
        if len(self.orders)>0:
            order = self.orders[0]
            self.orders.remove(order)
            self.motor_force = order.motor
            self.torque = order.turn
            return True
        else:
            return False

    def get_direction_vector(self):
        # Return a unit vector pointing in the ship's direction
        return Vector(math.cos(self.heading),
                      -math.sin(self.heading))

    def update(self, t):
        force_tot = self.motor_force - self.air_drag*self.airspeed
        acceleration = force_tot/self.mass
        torque_tot = self.torque - self.turn_drag*self.angular_freq
        rot_accel = torque_tot/self.moment_of_inertia
        print "Acceleration =", acceleration

        # Update ship speed using ship's acceleration
        self.airspeed = self.airspeed+acceleration*t
        self.angular_freq = self.angular_freq+rot_accel*t
        print "angular_freq:",self.angular_freq

    def move(self, t, wind):

        # Move the ship along its heading
        direction = self.get_direction_vector()
        self.position += direction*self.airspeed*t + wind

    def turn(self, t):
        # turn the ship according to its rotation
        self.heading += self.angular_freq*t

    def get_position_tuple(self):
        return (self.position.x, self.position.y)


class Map(object):
    def __init__(self, image, duplication=(1,1), position=None, ships=[], wind_direction = 0, windspeed=0):
        self.tile = pygame.image.load(image)
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


    def get_visible_rect(self):
        return pygame.Rect(self.position.x-SWIDTH//2,
                           self.position.y-SHEIGHT//2,
                           SWIDTH, SHEIGHT)

    def get_visible_surface(self):
        return self.surface.subsurface(self.get_visible_rect())

    def get_screen_coords(self, mapcoords):
        return (mapcoords-self.position+Vector(SWIDTH//2,SHEIGHT//2))


    def get_wind_vector(self):
        return self.windspeed*Vector(math.cos(self.wind_direction), math.sin(self.wind_direction))




def draw_background(map):
    screen.blit(map.get_visible_surface(), dest=(0,0))


def draw_action(screen, ships, blips, flip=True):
    # draw movement and action phase
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
            blip_pos = map.get_screen_coords(b[0])
            colors = [(255,0,0), (0,255,0), (0,0,255)]
            pygame.draw.circle(screen, colors[b[1]-1], blip_pos.tuple(), 3)

        text1 = font.render("Speed: %.2f Motor:%.2f Turn:%.2f Pos: (%d,%d)"%(ship.airspeed, ship.motor_force, math.degrees(ship.angular_freq), ship.position.x, ship.position.y), 1, (255,255,255))
        text2 = font.render("GAME ROUND:%d, STEP:%d"%(GAME_ROUND, STEP), 1, (255,255,0))

        screen.blit(text1, (5,5))
        screen.blit(text2, (5,25))
        if flip:
            pygame.display.flip()
        #print airship_rot.

def draw_strategy(justastring):
    # to be used for drawing interface and between action information, currently just filled with gibberish
    print justastring
    text1 = font.render('order 1', 1, (255,255,255))
    text2 = font.render('order 2', 1, (255,255,255))
    text3 = font.render('order 3', 1, (255,255,255))
    screen.blit(text1, (5,50))
    screen.blit(text2, (5,75))
    screen.blit(text3, (5,100))
    pygame.display.flip()


map = Map("forest.png", (1,1), windspeed=0.1, wind_direction=2*math.pi*random())
airship = Airship('airship.png', 'shadow.png', position=map.position)
font = pygame.font.Font(None, 36)
blips = []
mapcenter = MAP_CENTER
#delta_pos = Vector(0,0)
GAME_ROUND = 0
STEP = 0
orig_pos = airship.position
draw_action(screen, [airship], blips)

while 1:
    GAME_ROUND += 1

    last_motor = airship.motor_force
    last_turn = airship.torque

    for i in range(3):
        print "### GAME ROUND %d ###"%GAME_ROUND
        print "   --- ORDER #%d --- "%(i+1)
        motor = raw_input("   Motor speed, %d..%d [%.2f]:"%(
                airship.max_motor_force_backwards,
                airship.max_motor_force_forwards, last_motor))
        turn = raw_input("   Turn speed, %d..%d [%.2f]:"%(
                -airship.max_torque, airship.max_torque, last_turn))

        # Sanitize input
        if motor == "":
            motor = last_motor
        if turn == "":
            turn = last_turn
        motor, turn = float(motor), float(turn)
        motor = max(airship.max_motor_force_backwards,
                    min(motor, airship.max_motor_force_forwards))
        turn = max(-airship.max_torque, min(airship.max_torque, turn))

        order = Order(turn, motor)
        airship.give_order(order)

        last_motor, last_turn = motor, turn



    #ship_screen_pos = map.get_screen_coords(airship.position)
    #print "ship_screen_pos:", ship_screen_pos

    #### This is the user input loop
    # clicked = False
    # while not clicked:
    #     # we want a capped framerate to prevent flicker and CPU overheating...
    #     clock.tick(FRAMES_PER_SECOND)

    #     # check for mouse clicks
    #     for event in pygame.event.get():
    #         if event.type == MOUSEBUTTONDOWN:
    #             clicked = True

    #     # Figure out where the user clicked in relation to the ship
    #     mousepos = Vector(pygame.mouse.get_pos())
    #     airship_screenpos = map.get_screen_coords(airship.position)
    #     mousedir = mousepos - airship_screenpos
    #     mousedist = math.sqrt(mousedir.x**2 + mousedir.y**2)
    #     mouseangle = math.acos(mousedir.x/mousedist)
    #     if mousedir.y > 0:
    #         mouseangle = math.pi*2 - mouseangle

    #     mouseangle -= airship.heading
    #     if mouseangle > math.pi:
    #         mouseangle = -math.pi*2 + mouseangle
    #     elif mouseangle < -math.pi:
    #         mouseangle = math.pi*2 + mouseangle

    #     print mousedist , mouseangle

    #     draw_all(screen, [airship], blips, flip=False)

    #     pygame.draw.line(screen, (0,100,255),
    #                      airship_screenpos.tuple(),
    #                      (airship_screenpos+mousedir/mousedist*airship.speed).tuple(),
    #                      7)
    #     pygame.draw.line(screen, (255,0,0),
    #                      airship_screenpos.tuple(),
    #                      mousepos.tuple(), 3)

    #     pygame.display.flip()

    # airship.set_rotation( mouseangle )
    # airship.acceleration = max(-10, min(10, (mousedist-airship.speed)/20))
    # print airship.acceleration, airship.rotation

    #### And below is the "realtime" part

    #    blips = []

    #for i,t in enumerate(xrange(FRAMES_PER_SECOND*TURNTIME)):   # 100 ticks == 3 s
    i=t=0
    clicked = False
    map.wind_direction += random()-0.5

    while airship.carry_out_order():
        STEP += 1
        for i in range(TURNTIME * FRAMES_PER_SECOND):

            airship.update(1./FRAMES_PER_SECOND)

            # let's move the ship
            airship.move(1./FRAMES_PER_SECOND, map.get_wind_vector())
            # ...and turn it
            airship.turn(1./FRAMES_PER_SECOND)

            # add some markers each second, to show the ships movement
            if i%FRAMES_PER_SECOND == 0:
                blips.append((airship.position, STEP))

            # check if we need to scroll the background
            ship_screen_pos = map.get_screen_coords(airship.position)
            print "ship_screen_pos:", ship_screen_pos
            d = 0.3
            if ship_screen_pos.x > SWIDTH - SWIDTH*d:
                print "X+"
                map.position.x += ship_screen_pos.x - (SWIDTH - SWIDTH*d)
            if ship_screen_pos.x < SWIDTH * d:
                print "X-"
                map.position.x += ship_screen_pos.x - SWIDTH * d
            if ship_screen_pos.y > SHEIGHT - SHEIGHT * d:
                print "Y+"
                map.position.y += ship_screen_pos.y - (SHEIGHT - SHEIGHT * d)
            if ship_screen_pos.y < SHEIGHT * d:
                print "Y-"
                map.position.y += ship_screen_pos.y - SHEIGHT * d

            # update the screen
            draw_action(screen, [airship], blips)

            # move the time forward by one "tick"
            clock.tick(FRAMES_PER_SECOND)
            t += 1/FRAMES_PER_SECOND


            # Check if the user has clicked a mousebutton...
            # for event in pygame.event.get():
            #     if event.type == MOUSEBUTTONDOWN:
            #         clicked = True


    #delta_pos = airship.position - orig_pos

