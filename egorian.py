import os
import random
import mido
from random import choice, choices
from sys import argv
from collections import Counter 
from dataclasses import dataclass 
import json

@dataclass(frozen=True)
class Note:
  note: int
  duration: int
  def __repr__(self):
    return f"({self.note}, {self.duration})"

def midi_to_note_list(mid):
  messages = []
  last_dat = None
  last_msg = None
  for msg in mid.tracks[-1]:
    if msg.type == 'time_signature':
      print(msg)
    if msg.type == 'set_tempo':
      print('Tempo: ', msg.tempo)
    if msg.type == 'note_on':
      if msg.velocity == 0:
        dat = Note(last_msg.note, msg.time)
        messages.append(dat)
      else:
        last_msg = msg
  return messages

def count_note_pairs(note_lists):
  counts = {n : Counter() for n in sum(note_lists, [])}
  for notes in note_lists:
    for first, second in zip(notes, notes[1:]):
      counts[first][second] += 1

  return counts
      
def create_chain(mode):
  base = "../chants/" + mode
  chants = []
  for file in os.listdir(base):
    with mido.MidiFile(base+file) as mid:
      chants.append(midi_to_note_list(mid))

  pairs = count_note_pairs(chants)

def generate_track(chain):
  mid = mido.MidiFile(ticks_per_beat=192)
  track = mido.MidiTrack()
  mid.tracks.append(track)

  track.append(mido.Message('program_change', program=53, time=0))
  note = random.choice(list(pairs.keys()))
  while len(pairs[note]) != 0:
    print(note)
    note = random.choices(
        list(pairs[note].keys()),
        weights=list(pairs[note].values())
    )[0]
    track.append(mido.Message('note_on', note=note.note,velocity=127,time=0))
    track.append(mido.Message('note_on', note=note.note,velocity=0,time=note.duration))
  
  return mid


if __name__ == "__main__":
  base = "../chants/mode1/"
  chants = []
  for file in os.listdir(base):
    with mido.MidiFile(base+file) as mid:
      chants.append(midi_to_note_list(mid))

  pairs = count_note_pairs(chants)
  print(pairs)

  for first in pairs:
    for second in pairs[first]:
      assert(second in pairs)

  mid = generate_track('mode1')
  mid.save('mode1.mid')
  #print(msgs)
  #print(Counter(msgs))
