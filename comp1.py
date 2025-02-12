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
def build_major_triad(root):
    return chord.Chord([root, root + 4, root + 7])

# Build a 12-tone row from pcs, after which you can manipulate the row using
# other useful functions in the 'serial' module of the music21 library
p10 = serial.TwelveToneRow([10, 9, 4, 5, 6, 3, 2, 8, 7, 11, 0, 1]) 

def derive0(k):
    s = stream.Stream()
    d = duration.Duration(2.0)
    #test out derive 1
    s.insert(0, derive1(roman.RomanNumeral('I', k, duration = d)))
    
    s.append(roman.RomanNumeral('I7', k, duration = d))
    
    s.append(roman.RomanNumeral('IV7', k, duration = d))
    #test out drive 2
    s.append(6, derive2(roman.RomanNumeral('I', k, duration = d)))

    s.append(roman.RomanNumeral('V7', k, duration = d))
    
    s.append(roman.RomanNumeral('I', k, duration = d))
    return s


# x represents the chord within the stream you want to derive
def derive1(x):
    name = x.commonName
    if not(name == 'minor seventh chord' or name == 'minor triad' or name == 'dominant seventh chord' or name == 'major triad'):
        sys.stderr.write("derive1: Chord not recognized\n")
        return x
    expansion = stream.Stream()
    newDuration = duration.Duration(x.duration.quarterLength / 2)
    diminutedChord = (chord.Chord(x, duration = newDuration))
    expansion.append(diminutedChord)
    expansion.append(makeDominant(diminutedChord))
    return expansion.flatten()

# x represents the chord within the stream you want to derive
def derive2(x):
    name = x.commonName
    if not(name == 'minor seventh chord' or name == 'minor triad' or name == 'dominant seventh chord' or name == 'major triad'):
        sys.stderr.write("derive2: Chord not recognized\n")
        return x
    expansion = stream.Stream()
    newDuration = duration.Duration(x.duration.quarterLength / 2)
    diminutedChord = (chord.Chord(x, duration = newDuration))
    expansion.append(diminutedChord)
    expansion.append(roman.RomanNumeral('IV7', key.Key(x.root().name), duration = newDuration))
    return expansion.flatten()

def derive3a(w, x, minor):
    name = x.commonName
    if (name != 'dominant seventh chord'):
        sys.stderr.write("derive3a: unable to derive non-dominant chord\n")
        return x
    replacement = stream.Stream()
    domDuration = w.duration.quarterLength
    if (minor):
        replacement.append(roman.RomanNumeral('v7', key.Key(x.root().name), duration = domDuration))
    else:
        replacement.append(roman.RomanNumeral('V7', key.Key(x.root().name), duration = domDuration))
    replacement.append(x)
    return replacement.flatten()

def derive3b(w, x):
    name = x.commonName
    if (name != 'minor seventh chord'):
        sys.stderr.write("derive3a: unable to derive non-minor-dominant chord\n")
        return x
    replacement = stream.Stream()
    domDuration = w.duration.quarterLength
    replacement.append(roman.RomanNumeral('V7', key.Key(x.root().name), duration = domDuration))
    replacement.append(x)
    return replacement.flatten()

def derive4(d, x):
    
    name = x.commonName
    if not(name == 'minor seventh chord' or name == 'minor triad' or name == 'dominant seventh chord' or name == 'major triad'):
        sys.stderr.write("derive4: Chord not recognized\n")
        return x
    replacement = stream.Stream()
    superTonDuration = d.duration.quarterLength
    quality = x.quality
    if (quality == 'minor'):
        replacement.append(roman.RomanNumeral('ii-7', key.Key(x.root().name), duration = superTonDuration))
    else:
        replacement.append(roman.RomanNumeral('II-7', key.Key(x.root().name), duration = superTonDuration))
    replacement.append(x)
    return replacement.flatten()

def derive5(x):
    replacement = stream.Stream()
    replacement.append(x)
    replacement.append(roman.RomanNumeral('ii', key.Key(x.root().name), duration = x.duration.quarterLength))
    replacement.append(roman.RomanNumeral('iii', key.Key(x.root().name), duration = x.duration.quarterLength))
    return replacement.flatten()

def derive6(x, w):

def makeDominant(x):
    major_seventh_interval = interval.Interval("M7")
    major_seventh_note = major_seventh_interval.transposePitch(x.root())
    secondChord = chord.Chord(x)
    secondChord.add(major_seventh_note)
    return (secondChord)



def main():
    k = key.Key('C')
    s = derive0(k)
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
