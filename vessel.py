import math
import pygame

from vector import Vector
try:
    from PIL import Image, ImageChops
    import lighting
except ImportError:
    PIL_AVAILABLE = False
else:
    PIL_AVAILABLE=True

class Order(object):
    """
    An order given to a ship
    """
    def __init__(self, turn=0, motor=-1):
        self.turn = turn
        self.motor = motor

class Airship(pygame.sprite.Sprite):
    """
    A (sprite derived) class to describe an airship
    """
    if PIL_AVAILABLE:
        bumpmap = Image.open("airship_lightmap.png")
        lightmaps = []
        for i in range(10):
            lightmaps.append(lighting.get_lighting_overlay(bumpmap, i*math.pi/10))

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

        self.history = []


    def sanitize_angle(self, angle):
        # keeps an angle between 0 and 2 pi.
        if  angle > 2*math.pi:
            return angle - 2*math.pi
        elif angle < 0:
            return 2*math.pi + angle
        else:
            return angle


    def apply_lightmap(self):
        sun_direction = math.pi*0.75
        lighting_direction = self.sanitize_angle(self.heading+sun_direction)
        h = int(lighting_direction/(2*math.pi)*len(self.lightmaps*2))
        if 0 <= h < 10:
            lm = self.lightmaps[h]
        else:
            lm = self.lightmaps[10-h].transpose(Image.FLIP_TOP_BOTTOM)
        im = Image.fromstring("RGBA", self.image.get_size(), pygame.image.tostring(self.image, "RGBA"))
        img = im.convert("L")
        limg = ImageChops.multiply(img, lm).convert("RGBA")
        limg.putalpha(im.split()[-1])
        return pygame.image.frombuffer(limg.tostring(), self.image.get_size(), "RGBA")

    def get_surface(self, scale):
        """
        Create a surface containing the scaled and rotated ship + shadow
        """
        if PIL_AVAILABLE:
            image = self.apply_lightmap()
        else:
            image = self.image
        return (pygame.transform.rotozoom(image,
                                          math.degrees(-self.heading), scale),
                pygame.transform.rotozoom(self.shadowimage,
                                          math.degrees(-self.heading), scale))

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
                      math.sin(self.heading))

    def update_physics(self, t):
        force_tot = self.motor_force - self.air_drag*self.airspeed
        acceleration = force_tot/self.mass
        torque_tot = self.torque - self.turn_drag*self.angular_freq
        rot_accel = torque_tot/self.moment_of_inertia
        #print "Acceleration =", acceleration

        # Update ship speed using ship's acceleration
        self.airspeed = self.airspeed+acceleration*t
        self.angular_freq = self.angular_freq+rot_accel*t
        #print "angular_freq:",self.angular_freq

    def update(self, t, wind):
        self.update_physics(t)
        self.history.append(self.position)
        self.move(t, wind)
        self.turn(t)

    def move(self, t, wind):

        # Move the ship along its heading
        direction = self.get_direction_vector()
        self.position += direction*self.airspeed*t + wind

    def turn(self, t):
        # turn the ship according to its rotation
        self.heading = self.sanitize_angle(self.heading+self.angular_freq*t)

    def get_position_tuple(self):
        return (self.position.x, self.position.y)
