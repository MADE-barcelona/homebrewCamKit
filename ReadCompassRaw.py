
#!/usr/bin/env python

# Load the XLoBorg library
import XLoBorg

# Load maths library
import math

# Tell the library to disable diagnostic printouts
XLoBorg.printFunction = XLoBorg.NoPrint

# Start the XLoBorg module (sets up devices)
XLoBorg.Init()

# Read and display the raw magnetometer readings

mx,my,mz = XLoBorg.ReadCompassRaw()

print 'mX = %+06d, mY = %+06d, mZ = %+06d' % XLoBorg.ReadCompassRaw()

# get the heading in radians
heading = math.atan2 (my,mx)

# Correct negative values

if (heading < 0):
        heading  = heading + (2 * math.pi)

# convert to degrees

heading = heading * 180/math.pi;

print heading
