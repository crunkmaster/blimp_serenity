#!/usr/bin/python

# the program to connect roborealm and the blimp
import array
import time
import math
import os
from xbee import XBee, ZigBee
import serial

from collections import defaultdict
from RR_API import RR_API
import fiducials as fid

rr = RR_API()
rr.Connect("localhost")

# this needs to be changed to the correct COM port
PORT = '/dev/tty.usbserial-A601ETWD'
BAUD_RATE = 9600

ser = serial.Serial(PORT, BAUD_RATE)
xbee = ZigBee(ser, escaped=True)

# this needs to be changed to the correct destination address
DEST_ADDR_LONG = "\x00\x13\xA2\x00\x40\xAA\x18\xB2"
DEST_ADDR = "\xFF\xFF"

def send_references(x_reference, y_reference):
    xbee.tx(dest_addr_long=DEST_ADDR_LONG, dest_addr=DEST_ADDR,
            data="*{0},{1}".format(x_reference, y_reference))

while True:
    try:
        # get all variables from RR_API
        data = rr.GetAllVariables()
        fiducials = fid.get_fiducials(data)
        centers = fid.get_centers(fiducials)
        orientations = fid.get_orientations(fiducials)

        for i in xrange(0, len(centers)):
            orientation = orientations[i] * 1000
            simplex = int(round(centers[i][0]))
            simpley = int(round(centers[i][1]))

            print "x: {0}, y: {1}, angle: {2}".format(simplex, simpley, orientation / 1000)
            xbee.tx(dest_addr_long=DEST_ADDR_LONG, dest_addr=DEST_ADDR,
                    data="-{0},{1},{2}".format(simplex, simpley, orientation))    
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
