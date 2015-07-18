from midi import ParseMidi
from lib.MidiInFile import MidiInFile

# choose between real external hardware and a mockup
#import wiringpi2 as wpi
from mock import wpi

from time import sleep
import glob
import os
import ast
from time import time
from datetime import datetime
import timeit

# configuration
pin_base = 65
pin_last = 80
i2c_addr = 0x20
# how long a pin should be high/on in the test program, in seconds
on_duration = 0.2

# location of midi files
file_location = "../web/playlist/"
mapping_file = file_location + 'mapping'


# functions
def debug(text):
    if False:
        print text;

def pin_on(pin):
  debug("pin: "+str(pin)+" - on")
  wpi.digitalWrite(pin, 1)

def pin_off(pin):
  debug("pin: "+str(pin)+" - off")
  wpi.digitalWrite(pin, 0)

def all_on():
  for pin in xrange(pin_base, pin_last+1):
    pin_on(pin)

def all_off():
  for pin in xrange(pin_base, pin_last+1):
    pin_off(pin)

def playMidi(filename):
  debug("playing:" + filename)
  parser = ParseMidi()
  midi_in = MidiInFile(parser, filename)
  midi_in.read()

  allEvents = parser.getEvents()

  last = parser.getLast()

  mapping = {}
  try:
    if os.path.isfile(mapping_file):
      with open(mapping_file, 'r') as f:
        s = f.read()
        mapping = ast.literal_eval(s)
    else:
      debug("using default mapping")
  except:
    pass

  # provide default mapping
  if not mapping:
    mapping = {	36: 65, 
      37: 66, 
      38: 67,
      39: 71,
      40: 72,
      41: 73,
      42: 78,
      43: 79,
      44: 80}
  debug("mapping:"+str(mapping))

  total_start = timeit.default_timer()
  # iterate through all milliseconds
  for current_ms in xrange(0, last+1):
    start = timeit.default_timer()

    # check if events are to be processed
    try:
      events = allEvents[current_ms]
      # iterate over all events for this millisecond
      for event in events:
        # check if event contains note information
          if 'note' in event:
            # check if mapping to pin exists
            if event['note'] in mapping:
              pin = mapping[event['note']]
              # check if event contains on/off information
              if 'mode' in event:
                if event['mode'] == 0:
                  pin_off(pin)
                elif event['mode'] == 1:
                  pin_on(pin)
              else:
                debug("unknown mode in event:"+event)
            else:
              debug("no mapping for note:" + event['note'])
    except:
      pass

    end = timeit.default_timer()
    
    # fill the rest of the millisecond
    while (end-start) < (1.0/(1000.0)):
      end = timeit.default_timer()
  total_end = timeit.default_timer()
  #total_diff = 1000.0*(total_end-total_start)
  #skew = total_diff - last
  #print "total: " + str(total_diff)
  #print "last: " + str(last)
  #print("skew: "+str(skew))
def playTest():
  debug("testing")
  # toggle through all pins and turn them on shortly
  for pin in xrange(pin_base, pin_last+1):
    pin_on(pin)
    sleep(on_duration)
    pin_off(pin)

# setup wiring pi library to work with mcp23017
wpi.wiringPiSetup()
wpi.mcp23017Setup(pin_base, i2c_addr)

# set everything to outputs and set it low (off)
for pin in range(pin_base, pin_last+1):
  wpi.pinMode(pin, 1)
  pin_off(pin)

# main program
try:
  while True:
    # find files to be played
    for file in glob.glob(file_location+'*'):
      print "playing: "+file
      if file.endswith('.mid') or file.endswith('.midi'):
        playMidi(file)
        sleep(5)
      elif file.endswith('test'):
        playTest()
        sleep(5)
      elif file.endswith('exit'):
        os._exit(0)
    # sleep after playlist
    sleep(30)

finally:
  # turn all pins off
  all_off()
