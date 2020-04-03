import RPi.GPIO as GPIO
import time
import curses

# get the curses screen window
screen = curses.initscr()
# turn off input echoing
curses.noecho()
# respond to keys immediately (don't wait for enter)
curses.cbreak()
# map arrow keys to special values
screen.keypad(True)

##### assign GPIO ports
GPIO.setmode(GPIO.BCM)
LeftEnable  = 17
LeftFWD     = 27
LeftBKWD    = 22
RightEnable = 10
RightFWD    = 9
RightBKWD   = 11
redPort     = 21
greenPort   = 20
whitePort   = 16

##### motor variables
motorFrequency   = 100  # PWM motor frequency
leftSpeed   = 0    # minimum Duty Cycle to turn   
rightSpeed  = 0    #  motor is 22

##### LED variables
blinkFrequency = 5
off      = 0     # duty cycles
blink    = 50
on       = 100
 

# initialize GPIO ports
port = [LeftEnable, LeftFWD, LeftBKWD, RightEnable, RightFWD, RightBKWD, redPort, greenPort, whitePort]
for GPIOport in port:
   GPIO.setup(GPIOport, GPIO.OUT, initial=False)
   
MotorLeft = GPIO.PWM(LeftEnable,  motorFrequency)
MotorRight= GPIO.PWM(RightEnable, motorFrequency)
MotorLeft.start(leftSpeed)
MotorRight.start(rightSpeed)

redLed   = GPIO.PWM(redPort,   blinkFrequency)
greenLed = GPIO.PWM(greenPort, blinkFrequency)
whiteLed = GPIO.PWM(whitePort, blinkFrequency)
redLed.start(off)
greenLed.start(off)
whiteLed.start(off)

def leftIncr():    # key 7
    global leftSpeed
    if leftSpeed < 84:
       leftSpeed = leftSpeed + 1
       setLeftMotor(leftSpeed)
    return
   
def leftDecr():    # key 4
    global leftSpeed
    if leftSpeed > -84:
       leftSpeed = leftSpeed - 1
       setLeftMotor(leftSpeed)
    return
   
def rightIncr():    # key 9
    global rightSpeed
    if rightSpeed < 84:
       rightSpeed = rightSpeed + 1
       setRightMotor(rightSpeed)
    return
   
def rightDecr():    # key 6
    global rightSpeed
    if rightSpeed > -84:
       rightSpeed = rightSpeed - 1
       setRightMotor(rightSpeed)
    return

def forward():    # key 8
    global leftSpeed,rightSpeed
    if leftSpeed > rightSpeed:
       rightSpeed = leftSpeed
       setRightMotor(rightSpeed)
    elif rightSpeed > leftSpeed:
       leftSpeed = rightSpeed
       setLeftMotor(leftSpeed)
    else:
       leftIncr()
       rightIncr()     
    return

def backward():    # key 2
    global leftSpeed,rightSpeed
    if leftSpeed < rightSpeed:
       rightSpeed = leftSpeed
       setRightMotor(rightSpeed)
    elif rightSpeed < leftSpeed:
       leftSpeed = rightSpeed
       setLeftMotor(leftSpeed)
    else:
       leftDecr()
       rightDecr()     
    return    
      
   
def setLeftMotor(speed):
    if speed >= 0:
        GPIO.output(LeftFWD,True)
        GPIO.output(LeftBKWD,False)
    else:
        GPIO.output(LeftFWD,False)
        GPIO.output(LeftBKWD,True)
    if abs(speed) < 4:
       DC = 0
       GPIO.output(LeftFWD,False)
       GPIO.output(LeftBKWD,False)       
    else:   
       DC = abs(speed) + 16               
       MotorLeft.ChangeDutyCycle(DC)
       screen.addstr(1, 0, str(DC))
    return
   
def setRightMotor(speed):
    if speed >= 0:
        GPIO.output(RightFWD,True)
        GPIO.output(RightBKWD,False)
    else:
        GPIO.output(RightFWD,False)
        GPIO.output(RightBKWD,True)
    if abs(speed) < 4:
       DC = 0
       GPIO.output(RightFWD,False)
       GPIO.output(RightBKWD,False)       
    else:   
       DC = abs(speed) + 16               
       MotorRight.ChangeDutyCycle(DC)
       screen.addstr(1, 5, str(DC))
    return
   
def stopVehicle():    # key 5
    global leftSpeed,rightSpeed
    leftSpeed = 0
    rightSpeed = 0
    setLeftMotor(leftSpeed)
    setRightMotor(rightSpeed)
    return

def setLed(led, mode):
    # led: a shining PWM object
    # mode = [off, blink, on]
    if mode in [off, blink, on]:
        led.ChangeDutyCycle(mode)
    else:
        print(mode, ' is not a valid mode for function setLed')
    return

loop = True   
try:
    while loop:
        screen.addstr(0, 0, '                     ')
        screen.addstr(0, 0, str(leftSpeed))
        screen.addstr(0, 5, str(rightSpeed))
        char = screen.getkey()
        if char == 'q': 
            loop = False 
        elif char == '5':
            stopVehicle()
        elif char == '7':   
            leftIncr()
        elif char == '1':
            leftDecr()
        elif char == '9':
            rightIncr()
        elif char == '3':
            rightDecr()    
        elif char == '8':   # forward
            forward()  
        elif char == '2':   # backward
            backward()             
        elif char == '4':   # turn left
            leftDecr()
            rightIncr() 
        elif char == '6':   # turn right
            leftIncr()
            rightDecr()          
              
finally:
    # shut down cleanly
    MotorLeft.stop()
    MotorRight.stop()
    redLed.stop()
    greenLed.stop()
    whiteLed.stop()
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
