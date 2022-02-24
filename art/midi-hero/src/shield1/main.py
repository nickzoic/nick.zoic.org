import usb_midi
import digitalio
import analogio
import board

midi_out = usb_midi.ports[1]

knob = analogio.AnalogIn(board.A5)

button = digitalio.DigitalInOut(board.D7)
button.switch_to_input()

while True:
    # Just busy wait until the button gets pressed
    while not button.value: pass

    # Scale the 0..65535 range of the input to the 0..127 range
    # of MIDI notes (not very nicely)
    note = knob.value // 512

    # Play the note
    midi_out.write(bytes((0x90, note, 0x7F)))

    # Wait until the button gets released or the knob gets moved
    while button.value and (knob.value // 512 == note): pass

    # Cancel the old note, go back around and wait for next note.
    midi_out.write(bytes((0x80, note, 0x00)))
