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

# C 60 72
# C♯ 61 73
# D 62 74
# D♯ 63 75
# E 64 76
# F 65 77
# F♯ 66 78
# G 67 79
# G♯ 68 80
# A 69 81
# A♯ 70 82
# B 71 83

chords = {
        1: [ 60, 64, 67 ],      # 1, C
        2: [ 62, 66, 69 ],      # 2, D
        3: [ 62, 65, 69 ],      # 3, Dm
        4: [ 67, 71, 74 ],      # 4, G
        5: [ 64, 67, 71 ],      # 5, Em
        6: [ 65, 69, 72 ],      # 6, F
        7: [ 62, 66, 69, 73 ],  # 7, D7
        8: [ 69, 73, 76 ],      # 8, A
        10: [ 67, 70, 74 ],     # 10, Gm
        12: [ 69, 72, 64 ],     # 12, Am
        14: [ 67, 71, 74, 77 ], # 14, G7
        16: [ 71, 75, 78 ],     # 16, B
        20: [ 71, 74, 78 ],     # 20, Bm
        24: [ 70, 74, 77 ],     # 24, B♭
        28: [ 71, 75, 78, 81 ], # 28, B7
    }

def get_notes():
    val = ( (1 if not f_gn.value else 0) +
            (2 if not f_rd.value else 0) + 
            (4 if not f_yy.value else 0) +
            (8 if not f_bu.value else 0) +
            (16 if not f_or.value else 0) )
    return set(chords.get(val, []))

midi_out = usb_midi.ports[1]

while True:

    while s_up.value and s_dn.value: pass

    notes = get_notes()

    for note in notes:
        midi_out.write(bytes((0x90, note, 0x5f)))

    while not s_up.value or not s_dn.value: pass

    for note in notes:
        midi_out.write(bytes((0x80, note, 0)))

