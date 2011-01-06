from math import pi
from PIL import Image,  ImageFilter, ImageMath, ImageChops
from random import random

hs = [
    [[0,0,0],
     [-1,0,1],
     [0,0,0]],

    [[0,0,1],
     [0,0,0],
     [-1,0,0]],

    [[0,1,0],
     [0,0,0],
     [0,-1,0]],

    [[1,0,0],
     [0,0,0],
     [0,0,-1]],
    ]


def add_matrices(a, b, am=1, bm=1):
    # add two matrices together, optionally scaling each one first
    c = [[0,0,0], [0,0,0], [0,0,0]]
    for i in range(3):
        for j in range(3):
            c[i][j] = a[i][j]*am + b[i][j]*bm
    return c

def abs_matrix(a):
    # element-wise absolute value of a matrix
    b = [[0,0,0], [0,0,0], [0,0,0]]
    for i in range(3):
        for j in range(3):
            b[i][j] = abs(a[i][j])
    return b

def get_emboss_kernel(azimuth, elevation):
    # compute an 3x3 emboss kernel matrix for convolution
    az = 4*azimuth/pi  #convert angle to 0..8 for simplicity
    if 0 <= az <= 1:
        h = add_matrices(hs[1], hs[0], az, (1-az))
    elif 1 < az <= 2:
        h = add_matrices(hs[2], hs[1], (az-1), (2-az))
    elif 2 < az <= 3:
        h = add_matrices(hs[3], hs[2], (az-2), (3-az))
    elif 3 < az <= 4:
        h = add_matrices(hs[0], hs[3], -(az-3), (4-az))
    elif 4 < az <= 5:
        h = add_matrices(hs[1], hs[0], -(az-4), -(5-az))
    elif 5 < az <= 6:
        h = add_matrices(hs[2], hs[1], -(az-5), -(6-az))
    elif 6 < az <= 7:
        h = add_matrices(hs[3], hs[2], -(az-6), -(7-az))
    elif 7 <= az <= 8:
        h = add_matrices(hs[0], hs[3], (az-7), -(8-az))
    else:
        print "azimuth must be between 0 and 2*pi"
    return add_matrices(h, abs_matrix(h), 1, elevation)

#im = scipy.misc.imread(filename, flatten=True)
#im = 255*((1-(1-im/255)**2))   # convert linear to spherical gradient
#ha = get_emboss_kernel(pi*0.1, 0)
#for i in range(1):
#    im_out = scipy.signal.convolve2d(im, array(ha), 'same')
#scipy.misc.imshow(im_out)


def get_lighting_overlay(bumpmap, azimuth):
    azimuth = pi-azimuth
    ha = get_emboss_kernel(azimuth, 0.03)
    ImageFilter.EMBOSS.filterargs=((3, 3), 0.15, 150, reduce(lambda x, y: x+y, ha))

    im = bumpmap.convert("L")
    #im = 255*((1-(1-im/255)**2))   # convert linear to spherical gradient
    #im = Image.eval(im, lambda x: int(255*(1-(1-x/255.)**2)))

    for i in range(1):
        im1 = im.filter(ImageFilter.EMBOSS)
        #ImageMath.eval("min()")

    pixdata = im.getdata()
    for y in xrange(im1.size[1]):
        for x in xrange(im1.size[0]):
            if pixdata[x+im.size[0]*y] == 0:
                im1.putpixel((x,y), 255)

    return im1
    #im_final=ImageChops.multiply(im_airship_g, im1.offset(0,0))
    #im_final.putalpha(im_airship.split()[-1])

    #im_final.save("airshiptest.png")
