from __future__ import division

import sys
import pygame, time, math
from pygame.locals import *
from pygame import gfxdraw, Rect
from vector import Vector
from random import random
from pgu import gui

from interface import OrderControl
from vessel import Airship, Order
from world import Map

import util

pygame.init()

SWIDTH, SHEIGHT = 1024, 768
screen = pygame.display.set_mode((SWIDTH, SHEIGHT), SWSURFACE)

GREEN = (20,150,20)
MAP_CENTER = Vector(SWIDTH//2, SHEIGHT//2)
SCALE = 0.4
SCALE2 = 0.5

clock = pygame.time.Clock()
FRAMES_PER_SECOND = 30
TURNTIME = 3  # s

module_logger = util.get_module_logger(__name__)



def draw_background(world_map):
    screen.blit(world_map.get_visible_surface(), dest=(0,0))


def draw_action(screen, ships, flip=True):
    # draw movement and action phase
    #screen.fill(GREEN)
    draw_background(world_map)
    colors = [(255,0,0), (0,255,0), (0,0,255)]

    for i,ship in enumerate(ships):
        #airship.angle += 1
        airship_surf = ship.get_surface(scale=SCALE)
        #img_size = airship.get_surface_size()
        img_size = Vector(airship_surf[0].get_width(),
                          airship_surf[0].get_height())
        module_logger.debug("image size: " + str(img_size))
        module_logger.debug("map_coords:" +  str(world_map.get_screen_coords(ship.position)))
        screen.blit(airship_surf[1], (world_map.get_screen_coords(ship.position)-img_size/2+Vector(20,20)).tuple())
        screen.blit(airship_surf[0], (world_map.get_screen_coords(ship.position)-img_size/2).tuple())

        pathpoints=[]
        for j, b in enumerate(ship.history[-min(len(ship.history),1000)::10]):
            blip_pos = world_map.get_screen_coords(b)
            pathpoints.append(blip_pos.tuple())
            #pygame.draw.circle(screen, colors[i//3-1], map(int, blip_pos.tuple()), 3)
        if len(pathpoints) > 1:
            pygame.draw.lines(screen, colors[i], False, pathpoints, 3)
    text1 = font.render("Speed: %.2f Motor:%.2f Turn:%.2f Pos: (%d,%d)"%(ship.airspeed, ship.motor_force, math.degrees(ship.angular_freq), ship.position.x, ship.position.y), 1, (255,255,255))
    text2 = font.render("GAME ROUND:%d, STEP:%d"%(GAME_ROUND, STEP), 1, (255,255,0))

    screen.blit(text1, (250,5))
    screen.blit(text2, (250,25))
    if flip:
        pygame.display.flip()
    #print airship_rot.

def draw_strategy(themap):
    # draws arrow showing wind direciton
    windarrow = themap.get_windsurface(scale=SCALE2)
    screen.blit(windarrow, (25, 500))
    pygame.display.flip()


world_map = Map("dublin.jpg", "windarrow.png", (1,1), windspeed=0.1, wind_direction=2*math.pi*random())
airship1 = Airship('airship.png', position=world_map.position)
airship2 = Airship('Flecheairship.png', position=world_map.position+Vector(0,100))
airship3 = Airship('Vleermuisairship.png', position=world_map.position-Vector(0,100))
vessels = [airship1, airship2, airship3]

font = pygame.font.Font(None, 36)
blips = []
mapcenter = MAP_CENTER
#delta_pos = Vector(0,0)
GAME_ROUND = 0
STEP = 0
draw_action(screen, vessels)


# GUI stuff
form = gui.Form()
app = gui.App()
ordercontrol = OrderControl()
c = gui.Container(align=-1,valign=-1)
c.add(ordercontrol,0,0)
app.init(c)
print "lappskojs"

t=0

while 1:
    winddeg = world_map.change_wind()
    #print math.degrees(new_wind)
    module_logger.debug(math.degrees(winddeg))
    draw_strategy(world_map)
    GAME_ROUND += 1
    #print "Heading:", airship.heading

    # Order giving GUI loop

    while not ordercontrol.done:
        for e in pygame.event.get():
            if e.type is QUIT:
                done = True
            elif e.type is KEYDOWN and e.key == K_ESCAPE:
                done = True
            else:
                app.event(e)
        app.paint(screen)
        pygame.display.flip()

    ordercontrol.done = False
    module_logger.debug(form.items())
    vessels[0].give_order(Order(motor=form["speed1"].value, turn=form["turn1"].value))
    vessels[1].give_order(Order(motor=form["speed2"].value, turn=form["turn2"].value))
    vessels[2].give_order(Order(motor=form["speed3"].value, turn=form["turn3"].value))


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
    #     airship_screenpos = world_map.get_screen_coords(airship.position)
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

    for i in range(TURNTIME * FRAMES_PER_SECOND):
        for airship in vessels:
            if i==0:
                airship.carry_out_order()

            airship.update(1./FRAMES_PER_SECOND, world_map.get_wind_vector())

            # let's move the ship
            #airship.move(1./FRAMES_PER_SECOND, world_map.get_wind_vector())
            # ...and turn it
            #airship.turn(1./FRAMES_PER_SECOND)

            # add some markers each second, to show the ships movement


            # check if we need to scroll the background
            ship_screen_pos = world_map.get_screen_coords(airship.position)
            #print "ship_screen_pos:", ship_screen_pos
            d = 0.3
            if ship_screen_pos.x > SWIDTH - SWIDTH*d:
                #print "X+"
                world_map.position.x += ship_screen_pos.x - (SWIDTH - SWIDTH*d)
            if ship_screen_pos.x < SWIDTH * d:
                #print "X-"
                world_map.position.x += ship_screen_pos.x - SWIDTH * d
            if ship_screen_pos.y > SHEIGHT - SHEIGHT * d:
                #print "Y+"
                world_map.position.y += ship_screen_pos.y - (SHEIGHT - SHEIGHT * d)
            if ship_screen_pos.y < SHEIGHT * d:
                #print "Y-"
                world_map.position.y += ship_screen_pos.y - SHEIGHT * d

        # update the screen
        draw_action(screen, vessels)

        # move the time forward by one "tick"
        clock.tick(FRAMES_PER_SECOND)
        t += 1/FRAMES_PER_SECOND


        # Check if the user has clicked a mousebutton...
        # for event in pygame.event.get():
        #     if event.type == MOUSEBUTTONDOWN:
        #         clicked = True


    #delta_pos = airship.position - orig_pos

