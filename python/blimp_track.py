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
PORT = 'COM3'
BAUD_RATE = 9600

#ser = serial.Serial(PORT, BAUD_RATE)
#xbee = ZigBee(ser, escaped=True)

# this needs to be changed to the correct destination address
DEST_ADDR_LONG = "\x00\x13\xA2\x00\x40\xAA\x18\xB2"
DEST_ADDR = "\xFF\xFF"

def send_references(x_reference, y_reference):
    xbee.tx(dest_addr_long=DEST_ADDR_LONG, dest_addr=DEST_ADDR,
            data="*{0},{1}".format(x_reference, y_reference))

while True:
    try:
        # get all variables from RR_API
        x_r = 100
        y_r = 100
        data = rr.GetAllVariables()
        fiducials = rr.GetFiducials()
        fiducialsPath = rr.GetFiducialsPath()
        
        for key in fiducials.iterkeys():
            orientation = fid.get_orientation(fiducials[key])
            center = fid.get_center(fiducials[key]) 
            x = int(round(center[0]))
            y = int(round(center[1]))
            name = fid.get_fiducial_name(fiducials[key], fiducialsPath)
            scale = fid.get_scale(fiducials[key])
            
            print "x: {0} y: {1} orientation: {2} scale: {3}".format(x, y, orientation, scale)
            orientation = orientation * 10000
            scale = scale * 10000

#            xbee.tx(dest_addr_long=DEST_ADDR_LONG, dest_addr=DEST_ADDR,
#                    data="-{0},{1},{2}".format(simplex, simpley, orientation, scale))    
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
