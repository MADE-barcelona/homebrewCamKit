#!/usr/bin/python

from twisted.web import server, resource
from twisted.internet import reactor

import time
import XLoBorg
import math

try:
	import simplejson as json
except ImportError:
	import json

# Tell the library to disable diagnostic printouts
XLoBorg.printFunction = XLoBorg.NoPrint

# Start the XLoBorg module (sets up devices)
XLoBorg.Init()

class HelmetCam(resource.Resource):
    isLeaf = True
    print "starting"

    try:

    	def render_GET(self, request):
        	# Read and display the raw magnetometer readings
        	mx,my,mz = XLoBorg.ReadCompassRaw()

        	# get the heading in radians
       		heading = math.atan2 (my,mx)

        	# Correct negative values

        	if (heading < 0):
            		heading  = heading + (2 * math.pi)

        	# convert to degrees
        	heading = heading * 180/math.pi;

	        request.setHeader("content-type", "application/json")

		return json.dumps({"h": heading}) + "\n"

    except KeyboardInterrupt:
        pass


reactor.listenTCP(8081,server.Site(HelmetCam()))
reactor.run()

