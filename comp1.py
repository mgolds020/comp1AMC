#!/usr/bin/env python3
# Purpose: <TODO>
#
# This program currently just provides some code that you might find useful as
# you work on your first composition lab. Please remove this comment (and any
# unused starter code) and explain your actual program once you have a plan for
# your composition!
# 
# Author(s): <TODO>
# Date: <TODO>


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

def main():
    k = key.Key('C')
    Cmaj = build_triad(C_MIDI) #building a C major triad via midi values
    stream1 = stream.Stream()
    stream1.append(Cmaj)
    # Generating chords given a harmonic function and key
    stream1.append(roman.RomanNumeral('I', k))
    stream1.append(roman.RomanNumeral('V7', k))
    stream1.append(roman.RomanNumeral('VIIo7', k))
    # One stream can't have more than one of the same object at the same level of
    # stream hierarchy. So if I want to insert another Cmaj chord I have to 
    # generate a fresh one (see what happens if you just have "append(Cmaj)")!
    stream1.append(chord.Chord(Cmaj)) 

    # Let's kick things off with a banjo playing the chords
    stream1.insert(0, instrument.Banjo())
    # And then, assuming there are at least 4 chords, start playing the violin
    # from the 3rd onwards
    if len(stream1) > 2:
        stream1.insert(3, instrument.Violin())

    # Play midi, output sheet music, or print the contents of the stream
    print(len(stream1))
    if ("-m" in sys.argv):
        stream1.show('midi')
    elif ("-s" in sys.argv):
        stream1.show()
    else:
        stream1.show('text')

if __name__ == "__main__":
    main()
