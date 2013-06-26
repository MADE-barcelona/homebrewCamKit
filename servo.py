# Servo Control
import time

from twisted.web import server, resource
from twisted.internet import reactor

def set(prop, value):
    try:
	    f = open("/sys/class/rpi-pwm/pwm0/" + prop, 'w')
	    f.write(value)
	    print(prop + " value: " + value)
	    f.close()	
    except:
	    print("Error writing to: " + prop + " value: " + value)

def setServo(angle):
    set("servo", str(angle))

class CameraController(resource.Resource):
    
    isLeaf = 1
    position = 0
    percentage = 50
    
    body = "<H1>#POS#</H1>"
    
    print "initial position: ", position, type(position)
    
    def render_GET(self, request):

        # fetch page template.
        # camera.html     
        try:
            with open("camera.html") as myfile:
                self.body = "".join(line for line in myfile)
            myfile.closed
        except IOError:
            self.body = "<H1>#POS#</H1>oops..."
        
        newPosition = int(self.position)
        rawRequestedPosition = request.path                
               
        if rawRequestedPosition != "/favicon.ico":
            if rawRequestedPosition == "/LEFT":
                print "direction LEFT"
                newPosition = self.position + 1
            else: 
                if rawRequestedPosition == "/RIGHT":
                    print "direction RIGHT"
                    newPosition = self.position - 1
                else:
                    newPosition = int(filter(type(rawRequestedPosition).isdigit, rawRequestedPosition))
                    print "requested position" , request.path , type(filter(type(rawRequestedPosition).isdigit, rawRequestedPosition))

        print request.path , type(self.position), type(newPosition)
        
        if newPosition < 0:
            newPosition = 0
            
        if newPosition>180:        
            newPosition=180
            
        self.position = int(newPosition)
        
        self.percentage = 100 - (100 * float(self.position)/float(180))
        
        setServo(self.position)
        
        request.setHeader("content-type", "text/html")
        return self.body.replace("#POS#", str(self.position)).replace("#PCT#", str(self.percentage)).replace("#RPCT#",str(100- self.percentage))

    set("delayed", "0")
    set("mode", "servo")
    set("servo_max", "180")
    set("active", "1")
    setServo(position)

reactor.listenTCP(8080, server.Site(CameraController()))
print "Camera Controller started."
reactor.run()
