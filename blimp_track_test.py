#!/usr/bin/python

import array
import time
import math
import os
from xbee import XBee, ZigBee
import serial

from collections import defaultdict
import fiducials as fid

# this needs to be changed to the correct COM port
PORT = '/dev/tty.usbserial-A601ETWD'
BAUD_RATE = 9600

ser = serial.Serial(PORT, BAUD_RATE)
xbee = ZigBee(ser, escaped=True)

# this needs to be changed to the correct destination address
DEST_ADDR_LONG = "\x00\x13\xA2\x00\x40\xAA\x18\xB2"
DEST_ADDR = "\xFF\xFF"

while True:
    try:
        simplex = 0
        simpley = 0
        orientation = 3 * math.pi / 2
        print "x: {0}, y: {1}, angle: {2}".format(simplex, simpley, orientation)
        xbee.tx(dest_addr_long=DEST_ADDR_LONG, dest_addr=DEST_ADDR,
                data="-{0},{1},{2}".format(simplex, simpley, orientation * 10000))   x 
        time.sleep(.1)

    except KeyError:
        os.system('clear')
        print "no fiducial in vision"
        time.sleep(1)
        os.system('cls')
        pass

    except KeyboardInterrupt:
        print "all done"
        break

ser.close()

