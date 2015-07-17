The player uses the WiringPi library to control the MCP23017 and some MIDI lib that everybody seems to use but where i cant find the origin for parsing the MIDI information. The MIDI lib is stripped down and modified to my needs (simply parse the midi and return the information in an array instead of triggering events, see midi.py).

## Principle
The player is a python script which loops through all files in a special folder (the playlist). It plays each file and sleeps for a short period in between files. Once all files were played, it waits for a bit longer.

In order to achieve millisecond precision (which is dictated by MIDI), a busywaiting loop is employed. 

## Special configuration
Certain files are handled in a special manner by the player if found in the playlist

### Mapping
The mapping file can be used to change the relation between MIDI note and MCP23017 output. It is simply python notation, e.g.:

{36: 78, 37: 67, 38: 67, 39: 65, 40: 65, 41: 65, 42: 65, 43: 65, 44: 65}

meaning whenever MIDI note value 36 is played, the MCP23017 should activate its output 78.

### Test
When the player finds a file called ``test`` it simply plays all outputs.

### Exit
A file named ``exit`` will kill the player process which would otherwise loop through the playlist forever.
