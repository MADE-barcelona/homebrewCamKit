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
import urllib2

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
class CameraController():

    print "Camera Controller started."

    isLeaf = 1

    TICK = 6 # minimum degree of movement for servo.
    HOME = 90 # HOME position of the servo.

    position = HOME
    percentage = 50

    print "initial position: ", position, type(position)

    set("delayed", "0")
    set("mode", "servo")
    set("servo_max", "180")
    set("active", "1")
    setServo(position)

    def rotateCamera(self):

        newPosition = int(urllib2.urlopen("http://geekfreak.com:8080/").read())

        if newPosition < 0:
             newPosition = 0

        if newPosition > 180:
            newPosition = 180

        self.position = newPosition
        self.percentage = 100 - (100 * float(self.position)/float(180))
        
        print self.position
        setServo(self.position)

