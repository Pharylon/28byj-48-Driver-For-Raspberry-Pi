__author__ = 'Pharylon'

import time
import RPi.GPIO as GPIO
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-w", "--wait", type=float, default=0.001, help="Time to wait (in seconds) between steps. Default time is 0.001")
parser.add_argument("-s", "--steps", type=int, default=500, help="Number of steps to take. Default is 500, which is roughtly one revolution.")
parser.add_argument("-cc", "--counterclockwise", help="Turn stepper counterclockwise", action="store_true")
parser.add_argument("-v", "--verbose", help="Write pin actions", default=False, action="store_true")
args = parser.parse_args()


#We will be using GPIO pin numbers instead
#of phyisical pin numbers.
GPIO.setmode(GPIO.BCM)


#These are the four GPIO pins we will
#use to drive the stepper motor, in the order
#they are plugged into the controller board. So,
#GPIO 17 is plugged into Pin 1 on the stepper motor.
#If you change the pin hookup on the Pi, this is
#the only part of the code you should need to change.
GpioPins = [17, 18, 27, 22]


for pin in GpioPins:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, False)


#These steps are defined in datasheet at
#http://www.bitsbox.co.uk/data/motor/Stepper.pdf
#Each step is a list containing GPIO pins that should be set the High
StepSequence = range(0, 8)
StepSequence[0] = [GpioPins[0]]
StepSequence[1] = [GpioPins[0], GpioPins[1]]
StepSequence[2] = [GpioPins[1]]
StepSequence[3] = [GpioPins[1], GpioPins[2]]
StepSequence[4] = [GpioPins[2]]
StepSequence[5] = [GpioPins[2], GpioPins[3]]
StepSequence[6] = [GpioPins[3]]
StepSequence[7] = [GpioPins[3], GpioPins[0]]


#if we want the motor to run in "reverse" we flip the sequence order.
if args.counterclockwise:
	StepSequence.reverse()
	

curserSpin = ["/","-","|","\\","|"]
spinPosition = 0


#Just prints a spinning cursor. Used when --verbose not set to true.
def PrintCursorSpin():
	global curserSpin
	global spinPosition
	print "%s\r" % curserSpin[spinPosition],
	spinPosition += 1
	if spinPosition > 4:
		spinPosition = 0
		

#Print status of pins.		
def PrintStatus(enabledPins):
	if args.verbose:
		print "New Step:"
		for pin in GpioPins:
			if pin in enabledPins:
				print "Enabling Pin %i" % pin
			else:
				print "Disabling Pin %i" % pin
	else:
		PrintCursorSpin()


#The actual magic loop. Iterate through the pins turning them on and off.
stepsRemaining = args.steps
while stepsRemaining > 0:
    for pinList in StepSequence:
        for pin in GpioPins:
            if pin in pinList:
				GPIO.output(pin, True)
            else:
                GPIO.output(pin, False)
		PrintStatus(pinList)	
    	time.sleep(args.wait)
    stepsRemaining -= 1
	
