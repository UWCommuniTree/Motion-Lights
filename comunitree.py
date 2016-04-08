import time
import RPi.GPIO as GPIO

class Light(object):
    def __init__(self,x):
        self.number = x
        GPIO.setup(x,GPIO.OUT)
        self.pwmid = GPIO.PWM(x,1000)

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    lights = [18,23,24]
    brightness = 0 
    avgOf = 2
    leds = []
    # Sets up the lights to be turned on and off
    for count in range(len(lights)):
        leds.append(Light(lights[count]))
    for count in range(len(leds)):
        leds[count].pwmid.ChangeDutyCycle(brightness)
    stuff = []
    while True:
        dist = reading(0)
        stuff.append(dist)
        if(len(stuff)!=0 and len(stuff)%avgOf==0):
            brightness = blinkLights(stuff[-(avgOf):],leds,brightness,avgOf)
        print(brightness)

def reading(sensor):
    if(sensor==0):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12,GPIO.OUT)
        GPIO.setup(25,GPIO.IN)
        time.sleep(0.3)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(12, True)
        time.sleep(0.00001)
        GPIO.output(12, False)
        while GPIO.input(25) == 0:
          signaloff = time.time()
        while GPIO.input(25) == 1:
          signalon = time.time()
        timepassed = signalon - signaloff
        distance = timepassed * 17000
        return distance
        GPIO.cleanup()
    else:
        print ("Incorrect usonic() function varible.")

def blinkLights(stuff, a,bri,av):
    total = 0
    shit = 0
    for x in range(av):
        total+=stuff[x]
    average=total/av
    print(average)
    b=bri
    
    if(average<100):
        for l in range(100):
            if(b != 100):
                for x in range(len(a)):
                    a[x].pwmid.start(b)
                    time.sleep(.002)
                b+=1
    if(average>100 and b!=0):
        for l in range(100):
            for x in range(len(a)):
                a[x].pwmid.start(b)
                time.sleep(.002)
            b=b-1
    if(b==0):
        for x in range(len(a)):
            a[x].pwmid.stop()
    return b

try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
