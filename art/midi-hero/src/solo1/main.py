import usb_midi
import digitalio
import board

def make_button(pin):
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    return btn

s_up = make_button(board.D6)
s_dn = make_button(board.D7)

f_gn = make_button(board.D8)
f_rd = make_button(board.D9)
f_yy = make_button(board.D10)
f_bu = make_button(board.D11)
f_or = make_button(board.D12)

chords = {
        (True, False, False, False, False): [ 60 ],    # C
        (True, False, True, False, False): [ 61 ],     # C♯
        (True, True, False, False, False): [ 62 ],     # D
        (True, True, True, False, False): [ 63 ],      # D♯
        (False, True, False, False, False): [ 64 ],    # E
        (False, True, True, False, False): [ 65 ],     # F
        (False, True, False, True, False): [ 66 ],     # F♯
        (False, False, True, False, False): [ 67 ],    # G
        (False, False, True, False, True): [ 68 ],     # A♯
        (False, False, True, True, False): [ 69 ],     # A
        (False, False, False, True, True): [ 70 ],     # B♭
        (False, False, False, True, False): [ 71 ],    # B
        (False, False, False, False, True): [ 72 ],    # C
    }

midi_out = usb_midi.ports[1]

while True:

    while s_up.value and s_dn.value: pass

    notes = chords.get((not f_gn.value, not f_rd.value, not f_yy.value, not f_bu.value, not f_or.value), [])

    # play single notes on down, fifths on up
    if not s_up.value: notes = [ notes[0], notes[0] + 7 ]

    for note in notes:
        midi_out.write(bytes((0x90, note, 0x5f)))

    while not s_up.value or not s_dn.value: pass

    for note in notes:
        midi_out.write(bytes((0x80, note, 0)))

