import mido
from sys import argv

mid = mido.MidiFile(argv[1])
print(mid)
