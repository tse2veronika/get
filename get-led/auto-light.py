import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
p = 6
GPIO.setup(p, GPIO.IN)
state = 0
while True:
    if GPIO.input(p):
        GPIO.output(led, state)
        time.sleep(0.3)
    else:
        state = not state
        GPIO.output(led, state)
        time.sleep(0.3)
