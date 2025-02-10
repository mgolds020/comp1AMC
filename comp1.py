#!/usr/bin/env python3
# Purpose: Generate harmonies using Jazz Chord Sequences Grammer
#
# 
# Author(s): Jake Kerrigan and Milo Goldstien
# Date: 02/10/26


import sys
from music21 import *

#Useful Python functions (choice and choices) to randomly select something from
#a collection
from random import choice, choices 

C_MIDI = 60  #middle C in midi notation

# Given an integer representing a pitch in midi notation, build up a major triad
# with that pitch as the root.
def build_triad(root):
    return chord.Chord([root, root + 4, root + 7])

# Build a 12-tone row from pcs, after which you can manipulate the row using
# other useful functions in the 'serial' module of the music21 library
p10 = serial.TwelveToneRow([10, 9, 4, 5, 6, 3, 2, 8, 7, 11, 0, 1]) 

def derive0(s, k):
    d = duration.Duration(2.0)
    s.insert(0,(derive1(roman.RomanNumeral('I', k, duration = d))))
    s.append(roman.RomanNumeral('I7', k, duration = d))
    s.append(roman.RomanNumeral('IV7', k, duration = d))
    s.append(roman.RomanNumeral('I', k, duration = d))
    s.append(roman.RomanNumeral('V7', k, duration = d))
    s.append(roman.RomanNumeral('I', k, duration = d))


def derive1(x):
    expansion = stream.Stream()
    newDuration = duration.Duration(x.duration.quarterLength / 2)
    expansion.append(chord.Chord(x, duration = newDuration))
    major_seventh_interval = interval.Interval("M7")
    major_seventh_note = major_seventh_interval.transposePitch(x.root())
    secondChord = chord.Chord(x, duration = newDuration)
    secondChord.add(major_seventh_note)
    expansion.append(secondChord)
    return expansion.flatten()






def main():
    k = key.Key('C')
    s = stream.Stream()
    derive0(s, k)
    s = s.flatten()



    # Play midi, output sheet music, or print the contents of the stream
    print(len(s))
    if ("-m" in sys.argv):
        s.show('midi')
    elif ("-s" in sys.argv):
        s.show()
    else:
        s.show('text')

if __name__ == "__main__":
    main()
