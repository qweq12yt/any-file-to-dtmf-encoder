from fileinput import filename
import wave
import easygui
from math import sin, pi
from struct import pack

SILENCE = 50    # in milliseconds
TONE = 50       # in milliseconds

SAMPLE_RATE = 8000.0
TABLE = {0: (1209, 697), 1: (1336, 697), 2: (1477, 697), 3: (1633, 697), 4: (1209, 770), 5: (1336, 770), 6: (1477, 770), 7: (1633, 770), 8: (1209, 852), 9: (1336, 852), 10: (1477, 852), 11: (1633, 852), 12: (1209, 941), 13: (1336, 941), 14: (1477, 941), 15: (1633, 941)}

def silence(t=SILENCE):
    out = []
    n = t * (SAMPLE_RATE / 1000.0)
    for i in range(int(n)):
        out.append(0.0)
    return out

def tone(freq, t=TONE):
    out = []
    n = t * (SAMPLE_RATE / 1000.0)
    for i in range(int(n)):
        sample = sin(2 * pi * freq[0] * (i / SAMPLE_RATE)) / 2 + \
                 sin(2 * pi * freq[1] * (i / SAMPLE_RATE)) / 2
        out.append(sample)
    return out

def write_samples(file_like, samples):
    for sample in samples:
        file_like.writeframes(pack('h', int(sample * 32767.0)))

def encode_bfile(file, out):
    f = open(file, 'rb')
    while True:
        b = f.read(1)
        if b == b'':
            break

        h = int(hex(b[0]), base=16)
        h_n, l_n = h >> 4, h & 0x0F

        write_samples(out, tone(TABLE[h_n]))
        write_samples(out, silence())
        write_samples(out, tone(TABLE[l_n]))
        write_samples(out, silence())
    f.close()

file_name = easygui.fileopenbox('Chose file to encode', 'File selection')
if not file_name:
    exit(1)

out = wave.open(file_name.replace(file_name[file_name.index('.'):], '.wav'), 'w')
out.setparams((1, 2, SAMPLE_RATE, 0, 'NONE', 'not compressed'))
tones = encode_bfile(file_name, out)
out.close()
exit(0)