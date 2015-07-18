from midi import ParseMidi
from lib.MidiInFile import MidiInFile

#import wiringpi2 as wpi
from mock import wpi

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
# location of midi files
file_location = "../web/playlist/"
mapping_file = file_location + 'mapping'


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

def playMidi(filename):
  print "playing:", filename
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
      print "mapping file not found"
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
  print "m:", mapping

  print "last: ",last
  total_start = time()
  print('s: {0:.6f}'.format(total_start))
  # iterate through all milliseconds
  for current_ms in xrange(0, last+1):
    start = time()

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
                print "unknown mode in event:", event
            else:
              print "no mapping for note:", event['note']
    except:
      pass

    end = time()
    
    # fill the rest of the millisecond
    while (end-start) < (1.0/(1000.0)):
      end = time()
  total_end = time()
  print('e: {0:.6f}'.format(total_end))

def playTest():
  print "testing"
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
      print "f:"+file
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
