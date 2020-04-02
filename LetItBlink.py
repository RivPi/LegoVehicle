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

# assign GPIO ports
GPIO.setmode(GPIO.BCM)   # using BCM numbering
redPort     = 21
greenPort   = 20
whitePort   = 16

Frequency	= 5
loop = True
# duty cycles
off      = 0
blink    = 50
on       = 100

# initialize GPIO ports
port = [redPort, greenPort, whitePort]
for i in port:
   GPIO.setup(i, GPIO.OUT, initial=False)

# create PWM objects - Pulse Width Modulation
redLed = GPIO.PWM(redPort, Frequency)
greenLed = GPIO.PWM(greenPort, Frequency)
whiteLed = GPIO.PWM(whitePort, Frequency)
redLed.start(off)
greenLed.start(off)
whiteLed.start(off)

def setLed(led, mode):
    # led: a PWM object
    # mode = [off, blink, on]
    if mode in [off, blink, on]:
        led.ChangeDutyCycle(mode)
    else:
        print(mode, ' is not a vaiid mode for function setLed')
    return
led = greenLed
mode = off

try:
    while loop:
        ledstr = str(led)
        screen.addstr(0, 0, 'press a key')
        screen.addstr(1, 0, 'q: quit    5: execute')
        screen.addstr(3, 0, 'selected LED: '+ledstr)
        char = screen.getkey()
        if char == 'q':
            loop = False
        elif char == '7':
            led = redLed
        elif char == '8':
            led = whiteLed
        elif char == '9':
            led = greenLed
       	elif char == '1':
            mode = off
        elif char == '2':
            mode = blink
        elif char == '3':
	        mode = on
        elif char == '5':
    	    setLed(led,mode)


finally:
    # shut down cleanly
    greenLed.stop()
    redLed.stop()
    whiteLed.stop()
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
