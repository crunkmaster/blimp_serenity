#!/usr/bin/env python

import subprocess
import serial
import time
from xbee import XBee, ZigBee


# set up xbee for communication
# PORT = 'COM3'
# BAUD_RATE = 9600

# ser = serial.Serial(PORT, BAUD_RATE)
# xbee = ZigBee(ser, escaped=True)

# # this should be changed to the correct address
# DEST_ADDR_LONG = "\x00\x13\xA2\x00\x40\xAA\x18\xD5"
# DEST_ADDR = "\xFF\xFF"

# set up subprocess to communicate with camera tracking
proc = subprocess.Popen('./camera_track_test', stdout=subprocess.PIPE)

x = 0
y = 0

# grab output lines from proc and use them
while True:
    line = proc.stdout.readline()
    x, y = line.split()
    print "x: {0}, y: {1}".format(x, y)
    # send over to xbee
#    xbee.tx(dest_addr_long=DEST_ADDR_LONG, dest_addr=DEST_ADDR,
#            data="-{0},{1}".format(x, y))
    time.sleep(.1)

ser.close()
