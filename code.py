import board
import digitalio
import pwmio
import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

print("MacroPad MIDI Board")

button_pins = [board.GP0,board.GP1,board.GP2, board.GP3,board.GP4,board.GP5,board.GP6,board.GP7]
keys = [['ENT', '0', 'ESC', 'ONOFF'],
['7', '8', '9', 'LOCK'],
['4', '5', '6', 'GO'],
['1', '2', '3', 'STOP']
]

rows = [board.GP4, board.GP5, board.GP6, board.GP7]
columns = [board.GP0, board.GP1, board.GP2, board.GP3]

keypad_rows = []
keypad_columns = []

for i in rows:
    keypad_rows.append(digitalio.DigitalInOut(i))

for i in columns:
    keypad_columns.append(digitalio.DigitalInOut(i))

col_pins = []
row_pins = []


for pin in keypad_rows:
    pin.direction = digitalio.Direction.OUTPUT
    pin.value = False
    row_pins.append(pin)

for pin in keypad_columns:
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP
    col_pins.append(pin)

notes= [['F3', 'G3', 'A3', 'B3'],
['C3', 'D3', 'E3', 'D4'],
['G4', 'A5', 'B5', 'C5'],
['D5', 'E5', 'F6', 'G6']
]

def fix_layout(to_fix):
    n=len(to_fix)
    fixed=[[-1] for _ in range(n)]
    for i in range(n):
        fixed[(i+n-1)%n]=to_fix[i]
    return fixed
note_mapping=fix_layout(notes)
keys_pressed = [[False for _ in range(4)] for _ in range(4)]
def scankeys():
    for row in range(0, 4):
        for col in range(0, 4):
            row_pins[row].value = False
            key = None

            key_press = note_mapping[row][col]
            if col_pins[col].value == False and keys_pressed[row][col]==False:
                keys_pressed[row][col] = True
                print("You have pressed:", keys[row][col], key_press)
                midi.send(NoteOn(key_press, 60))

            if col_pins[col].value == True and keys_pressed[row][col] == True:
                keys_pressed[row][col] = False
                midi.send(NoteOff(key_press, 0))
        row_pins[row].value = True

while True:
    scankeys()
