####################################################################
#
#   Copyright (c) 2013 MADE-BCN
#   All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#   2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#   ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#   WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#   DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#   ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#   (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#   LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#   ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#   SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#   The views and conclusions contained in the software and documentation are those
#   of the authors and should not be interpreted as representing official policies,
#   either expressed or implied, of MADE-BCN.
#
####################################################################

import time

# twisted web server
# sudo apt-get install python-twisted
from twisted.web import server, resource
from twisted.internet import reactor

##################################################
#   Utility functions to access the PWM mode on
#   pin 18 of the raspberry pi
##################################################
def set(prop, value):
    try:
        f = open("/sys/class/rpi-pwm/pwm0/" + prop, 'w')
        f.write(value)
        f.close()
    except:
        print("Error writing to: " + prop + " value: " + value)

def setServo(angle):
    set("servo", str(angle))

##################################################
#   Basic camera controller
##################################################
class CameraController(resource.Resource):

    print "Camera Controller started."

    isLeaf = 1

    TICK = 6 # minimum degree of movement for servo.
    HOME = 90 # HOME position of the servo.

    position = HOME
    percentage = 50

    body = "<H1>#POS#</H1>" # Worst case scenario!

    print "initial position: ", position, type(position)

    set("delayed", "0")
    set("mode", "servo")
    set("servo_max", "180")
    set("active", "1")
    setServo(position)

    def render_GET(self, request):

        ###################################################
        #   fetch page template.
        #   camera.html is reloaded with every request
        #   in an apparent homage to 1998! but allows very
        #   rapid change/deploy for the web UI.
        ###################################################
        try:
            with open("camera.html") as myfile:
                self.body = "".join(line for line in myfile)
            myfile.closed
        except IOError:
            self.body = "<H1>#POS#</H1>oops..."

        ####################################################
        #   Simple HTTP get API
        #
        #   http://HOSTNAME:8080
        #       reset to HOME position
        #   http://HOSTNAME:8080/nnn
        #       where nnn is a value between 0 and 180
        #   http://HOSTNAME:8080/LEFT
        #   http://HOSTNAME:8080/RIGHT
        #       to tick the motor left or right
        #
        ####################################################
        newPosition = int(self.position)
        rawRequestedPosition = request.path

        if rawRequestedPosition != "/favicon.ico":

            print request.getClientIP(), request.uri ,

            if request.uri  == "/": # send to HOME position
                newPosition = self.HOME
            elif rawRequestedPosition == "/LEFT":
                newPosition = self.position + self.TICK
            elif rawRequestedPosition == "/RIGHT":
                newPosition = self.position - self.TICK
            else:
                try:
                    newPosition = int(filter(type(rawRequestedPosition).isdigit, rawRequestedPosition))
                except ValueError:
                    newPosition = self.position
                    print "***" ,

            print type(self.position), self.position, type(newPosition) , newPosition

            if newPosition < 0:
                newPosition = 0

            if newPosition > 180:
                newPosition = 180

            self.position = int(newPosition)

            self.percentage = 100 - (100 * float(self.position)/float(180))

            setServo(self.position)

        request.setHeader("content-type", "text/html")
        return self.body.replace("#POS#", str(self.position)).replace("#PCT#", str(self.percentage)).replace("#RPCT#",str(100- self.percentage))

reactor.listenTCP(8080, server.Site(CameraController()))
reactor.run()
