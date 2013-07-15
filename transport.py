#!/usr/bin/env python
import subprocess
import serial
import time
import math
from xbee import XBee, ZigBee

# # set up xbee for communication
# PORT = '/dev/tty.usbserial-A601EYOI'
# BAUD_RATE = 9600

# ser = serial.Serial(PORT, BAUD_RATE)
# xbee = ZigBee(ser, escaped=True)

# # this should be changed to the correct address
# DEST_ADDR_LONG = "\x00\x13\xA2\x00\x40\xAA\x18\xD5"
# DEST_ADDR = "\xFF\xFF"

# set up subprocess to communicate with camera tracking
proc = subprocess.Popen('./blimp_track', stdout=subprocess.PIPE)

blue_x = 0
blue_y = 0

red_x = 0
red_y = 0

x_r = 30
y_r = 30

# grab output lines from proc and use them
while True:
    line = proc.stdout.readline()

    blue_x, blue_y, red_x, red_y = line.split()
    blue = {'x': int(blue_x), 'y': int(blue_y)}
    red = {'x': int(red_x), 'y': int(red_y)}

    if blue['x'] == -2147483648:
        print "cannot see blue object"
    elif red['x'] == -2147483648:
        print "cannot see red object"
    else:
        average_x = (blue['x'] + red['x']) / 2
        average_y = (blue['y'] + red['y']) / 2
        print "x: {0}, y: {1}".format(average_x, average_y)

        # this is an orientation between -pi and pi radians
        orientation = math.atan2(blue['y'] - red['y'], blue['x'] - red['x'])
        print "orientation: {0}".format(orientation)
        # this is designed to send the information that the arduino code is expecting
        # x_r, y_r, currentx, currenty, orientation
        # xbee.tx(dest_addr_long=DEST_ADDR_LONG, dest_addr=DEST_ADDR,
        #         data="-{0},{1},{2},{3},{4}".format(x_r, y_r, average_x, average_y, orientation))
ser.close()
