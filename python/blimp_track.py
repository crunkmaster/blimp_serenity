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
PORT = 'COM11'
BAUD_RATE = 9600

ser = serial.Serial(PORT, BAUD_RATE)
xbee = ZigBee(ser, escaped=False)

# this needs to be changed to the correct destination address
DEST_ADDR_LONG = "\x00\x13\xA2\x00\x40\xAA\x18\xB2"
DEST_ADDR = "\xFF\xFF"

# create a logfile with a name based on the time the program
# was run...
timestr = time.strftime("%Y%m%d-%H%M%S") 
logfile = open("{}.csv".format(timestr), 'w')

def send_references(x_reference, y_reference):
    xbee.tx(dest_addr_long=DEST_ADDR_LONG, dest_addr=DEST_ADDR,
            data="*{0},{1}".format(x_reference, y_reference))

# create the header for the CSV log file
logfile.write("X,Y,ORIENTATION,SCALE,TIME\n")

while True:
    try:
        # get all variables from RR_API
        x_r = 100
        y_r = 100
        vel_angular = 0
        orientation_stored = 0
        orientation_current = 0
        flag = 0
        data = rr.GetAllVariables()
        fiducials = rr.GetFiducials()
        fiducialsPath = rr.GetFiducialsPath()
        
        for key in fiducials.iterkeys():
            orientation = fid.get_orientation(fiducials[key])
            # velocity calculations
            if flag == 0:
                orientation_stored = orientation
                flag = 1
            if flag == 1:
                vel_angular = (orientation - orientation_stored) / .1
                if vel_angular > 50 or vel_angular < -50:
                    if orientation > orientation_stored:
                        vel_angular = (2.0 * math.pi - (orientation - orientation_stored)) / .1
                    else:
                        vel_angular = (-2.0* math.pi - (orientation - orientation_stored)) / .1
                flag = 0
                    
            center = fid.get_center(fiducials[key]) 
            x = int(round(center[0]))
            y = int(round(center[1]))
            name = fid.get_fiducial_name(fiducials[key], fiducialsPath)
            scale = fid.get_scale(fiducials[key])
            
            print "x: {0} y: {1} orientation: {2} scale: {3}".format(x, y, orientation, scale)
            print "vel_angular: {0} last orientation: {1}".format(vel_angular, orientation_stored )
            orientation = int(orientation * 10000)
            vel_angular = int(vel_angular * 10000)
            scale = int(scale * 10000)

            # write everything out to the CSV file
            timestamp = time.time()
            logfile.write("{},{},{},{},{}\n".format(x, y, orientation, scale, timestamp))

            xbee.tx(dest_addr_long=DEST_ADDR_LONG, dest_addr=DEST_ADDR,
                    data="-{0},{1},{2},{3}".format(x, y, orientation, scale))
            time.sleep(.1)

    # I think this stopped being useful after an update to roborealm...
    except KeyError:
        os.system('clear')
        print "no fiducial in vision"
        time.sleep(1)
        os.system('cls')
        pass
    except ValueError:
        print "value error"
        x = 0
        y = 0
        orientation = 0
        scale = 100 * 10000
        xbee.tx(dest_addr_long=DEST_ADDR_LONG, dest_addr=DEST_ADDR,
                data="-{0},{1},{2},{3}".format(x, y, orientation, scale))
        time.sleep(.1)
        pass
    except KeyboardInterrupt:
        print "all done"
        break

ser.close()
logfile.close()