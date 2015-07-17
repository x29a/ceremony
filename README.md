This is the code that drives the art project "Ceremony" by Anne Pfeifer (http://www.annepfeifer.com).

## Ceremony
Ceremony is an art installation consisting of 9 wooden boxes that are mounted on a wall in an arrangement of 3 x 3. Solenoids within the boxes can hit the boxes that are lined with various materials which produces a special and different sound on each box. Since the boxes are mounted on springs, they generate great accoustics and keep bouncing, even when the solenoids are turned off.

## Components
The installation consists of multiple components of which the technical ones are covered here.

### CPU
The core of the electronic part is a Raspberry Pi (Model B), equipped with an TP-Link 725N USB Dongle. A stripped down headless version of raspbian is used.

### Driver
The nine solenoids are driven by an MCP23017 which is connected via SPI to the RPi. The digital outputs are then amplified with TODO and directly power the solenoids

### Webinterface
The WLAN dongle creates a special (protected) adhoc WiFi (hostapd + udhcpd) where the configuration can be performed via e.g. laptop or smartphone.

### Player
As input format, MIDI was chosen, so each note relates with a solenoid. This way, it is really easy to command the length and the timing of impulses. A player implemented in python parses the MIDI file and then commands the solenoids.
