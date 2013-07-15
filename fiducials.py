# some functions for dealing with fiducials
# a useful abstraction...

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

