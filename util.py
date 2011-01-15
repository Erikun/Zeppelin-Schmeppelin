import logging
import math

import pygame
try:
    from PIL import Image
except ImportError:
    PIL_AVAILABLE = False
else:
    PIL_AVAILABLE=False


#The file name where log output is written
LOG_FILENAME = "output.log"
#Set which level of logging should be done.possible values:
# logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logging.basicConfig(filename = LOG_FILENAME, level = logging.DEBUG)

def get_module_logger(module_name):
    module_logger = logging.getLogger(module_name)
    return module_logger


def sanitize_angle(angle):
    # keeps an angle between 0 and 2 pi.
    if  angle > 2*math.pi:
        return angle - 2*math.pi
    elif angle < 0:
        return 2*math.pi + angle
    else:
        return angle

def get_pil_image(image):
    return Image.fromstring("RGBA", image.get_size(), pygame.image.tostring(image, "RGBA"))
