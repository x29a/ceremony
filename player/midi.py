from lib.MidiOutStream import MidiOutStream
from lib.MidiInFile import MidiInFile
from lib.MidiToText import MidiToText

from time import time
import os

# class overloads midi events to parse it into data structure
class ParseMidi(MidiOutStream):
	def __init__(self):
		self._total_dur = 0
		self._events = {} 
		self._last_event = 0

	def note_on(self, channel=0, note=0x40, velocity=0x40):
		self.addEvent(self.abs_time(), channel, note, velocity, 1)

	def note_off(self, channel=0, note=0x40, velocity=0x40):
		self.addEvent(self.abs_time(), channel, note, velocity, 0)

	def addEvent(self, abs_time, channel, note, velocity, mode):
		# save time of last event
		self._last_event = abs_time
	  
		# generate event
		event = {'channel': channel, 'note': note, 'velocity': velocity, 'mode': mode}
	  
		# debug
		#print event

		events = []
		# check if there are events at this time already
		try:
		  events = self._events[abs_time]

		except:
		  # there was no entry yet
		  pass
		#print "fresh event"

		# add the event to the events
		events.append(event)

		# add the events to the timeline
		self._events[abs_time] = events


	def getEvents(self):
		return self._events

	def getLast(self):
		return self._last_event

