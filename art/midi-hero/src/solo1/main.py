import usb_midi
import digitalio
import analogio
import board

def make_button(pin):
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.DOWN
    return btn

fret_green = make_button(board.D2)
fret_red = make_button(board.D3)
fret_yellow = make_button(board.D4)
fret_blue = make_button(board.D5)
fret_orange = make_button(board.D6)

button_select = make_button(board.D8)
button_start = make_button(board.D9)

strum_down = make_button(board.D10)
strum_up = make_button(board.D11)

pitch_wheel = analogio.AnalogIn(board.A0)

notes = {
        (True, False, False, False, False): 60,    # C
        (True, False, True, False, False):  61,     # C♯
        (True, True, False, False, False):  62,     # D
        (True, True, True, False, False):   63,      # D♯
        (False, True, False, False, False): 64,    # E
        (False, True, True, False, False):  65,     # F
        (False, True, False, True, False):  66,     # F♯
        (False, False, True, False, False): 67,    # G
        (False, False, True, False, True):  68,     # A♯
        (False, False, True, True, False):  69,     # A
        (False, False, False, True, True):  70,     # B♭
        (False, False, False, True, False): 71,    # B
        (False, False, False, False, True): 72,    # C
    }

midi_out = usb_midi.ports[1]

# All notes off
midi_out.write(bytes((0xb0, 123, 0)))

while True:

    while not strum_up.value and not strum_down.value: pass

    frets = (fret_green.value, fret_red.value, fret_yellow.value, fret_blue.value, fret_orange.value)
    note = notes.get(frets, None)
    
    if note is not None:
        if strum_up.value: note = note + 12
        print(note)

        midi_out.write(bytes((0x90, note, 0x3f)))

        while strum_up.value or strum_down.value:
            
            pitch_down = (65000 - pitch_wheel.value) >> 3
            if pitch_down < 0: pitch_down = 0
            
            pitch_down = 0x2000 - pitch_down
            print(pitch_down)
            pitch_l = pitch_down & 0x7F
            pitch_h = pitch_down >> 7
            midi_out.write(bytes((0xE0, pitch_l, pitch_h)))
            
        midi_out.write(bytes((0x80, note, 0)))

