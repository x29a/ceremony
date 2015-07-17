import wiringpi2 as wpi
from time import sleep
import glob
import os
import ast
from time import time

# configuration
pin_base = 65
pin_last = 80
i2c_addr = 0x20
# how long a pin should be high/on, in seconds
on_duration = 0.2


# functions
def pin_on(pin):
	print "pin: "+str(pin)+" - on"
	wpi.digitalWrite(pin, 1)

def pin_off(pin):
	print "pin: "+str(pin)+" - off"
	wpi.digitalWrite(pin, 0)

def all_on():
	for pin in xrange(pin_base, pin_last+1):
		pin_on(pin)
def all_off():
	for pin in xrange(pin_base, pin_last+1):
		pin_off(pin)

# setup wiring pi library to work with mcp23017
wpi.wiringPiSetup()
wpi.mcp23017Setup(pin_base, i2c_addr)

try:
  all_off()

finally:
  all_off()
