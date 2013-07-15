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

rr = RR_API()
rr.Connect("localhost")

# this needs to be changed to the correct COM port
PORT = 'COM3'
BAUD_RATE = 9600

ser = serial.Serial(PORT, BAUD_RATE)
xbee = ZigBee(ser, escaped=True)

# this needs to be changed to the correct destination address
DEST_ADDR_LONG = "\x00\x13\xA2\x00\x40\xAA\x18\xD5"
DEST_ADDR = "\xFF\xFF"

while True:
    try:
        # get all variables from RR_API
        data = rr.GetAllVariables()
        fiducials = get_fiducials(data)
        centers = get_centers(fiducials)
        orientations = get_orientations(fiducials)

        for i in xrange(0, len(centers)):
            # multiplied by 1000 so that on the arduino to avoid parseFloat
            orientation = orientations[i] * 1000
            simplex = int(round(centers[i][0]))
            simplex = int(round(centers[i][1]))
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

def get_fiducials(data):
    fiducials = data['FIDUCIALS'].split(',')
    fiducials = map(float, fiducials)
    fiducialMatrix = [[fiducials[j] for j in range( (i*17), (i*17) + 17 )]
                      for i in range(0, (len(fiducials) /17))]

    fiducialDict = {}
    for i in xrange(0, (len(fiducials) / 17)):
        fiducialDict['FID{0}'.format(i + 1)] = fiducialMatrix[i]

    return fiducialDict

def get_centers(fiducialDict):
    centers = []
    for key in sorted(fiducialDict.iterkeys() ):
        xs = fiducialDict[key][1:8:2] # slice the x coordinates
        ys = fiducialDict[key][2:9:2] # slice the y coordiantes
        centers.append( [sum(xs) / len(xs), sum(ys) / len(ys)] )

    return centers

def get_orientations(fiducialDict):
    orientations = []
    for key in sorted(fiducialDict.iterkeys() ):
        orientations.append( fiducialDict[key][14] * (math.pi / 180) )

    return orientations
    
