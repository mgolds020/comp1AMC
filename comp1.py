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
    d = duration.Duration(8.0)

    #test out derive 1
    s.append(roman.RomanNumeral('I', k, duration = d))
    
    s.append(roman.RomanNumeral('I7[b7]', k, duration = d))
    
    s.append(roman.RomanNumeral('IV7[b7]', k, duration = d))

    s.append(roman.RomanNumeral('I', k, duration = d))

    s.append(roman.RomanNumeral('V7', k, duration = d))
    
    s.append(roman.RomanNumeral('I', k, duration = d))

    return s

# def applyDerive4(s):
#     lastChord = None
#     for chord in s.recurse():
#         if(lastChord):
#             el

def applyDerive1(s):
    index = choice(range(len(s)))
    chordToDerive = s[index]
    while(chordToDerive.duration.quarterLength < 4.0):
        index = choice(range(len(s)))
        chordToDerive = s[index]
    offset = chordToDerive.offset
    s.pop(index)
    s.insert(offset, derive1(chordToDerive))
    s = s.flatten()

def applyDerive2(s):
    index = choice(range(len(s)))
    chordToDerive = s[index]
    while(chordToDerive.duration.quarterLength < 4.0):
        index = choice(range(len(s)))
        chordToDerive = s[index]
    offset = chordToDerive.offset
    s.pop(index)
    s.insert(offset, derive2(chordToDerive))
    s = s.flatten()

def applyDerive3a(s):
    index = choice(range(len(s) - 1))
    chordToDerive = s[index]
    nextChordToDerive = s[(index + 1)]
    while(chordToDerive.duration.quarterLength < 4.0):
        index = choice(range(len(s) - 1))
        chordToDerive = s[index]
    offset = chordToDerive.offset
    s.pop(index + 1)
    s.pop(index)
    isMinor = choice(range(1))
    s.insert(offset, derive3a(chordToDerive, nextChordToDerive, isMinor))
    s = s.flatten()


# x represents the chord within the stream you want to derive
#splits and adds minor 7
def derive1(x):
    name = x.commonName
    if not(name == 'minor seventh chord' or name == 'minor triad' or name == 'dominant seventh chord' or name == 'major triad'):
        sys.stderr.write("derive1: Chord not recognized\n")
        return x
    expansion = stream.Stream()
    newDuration = duration.Duration(x.duration.quarterLength / 2)
    diminutedChord = (chord.Chord(x, duration = newDuration))
    expansion.append(diminutedChord)
    expansion.append(roman.RomanNumeral('I-7', key.Key(diminutedChord.root().name), duration = newDuration))
    return expansion.flatten()

# x represents the chord within the stream you want to derive
# splits and add the 4
def derive2(x):
    name = x.commonName
    if not(name == 'minor seventh chord' or name == 'minor triad' or name == 'dominant seventh chord' or name == 'major triad'):
        sys.stderr.write("derive2: Chord not recognized\n")
        return x
    expansion = stream.Stream()
    newDuration = duration.Duration(x.duration.quarterLength / 2)
    diminutedChord = (chord.Chord(x, duration = newDuration))
    expansion.append(diminutedChord)
    expansion.append(roman.RomanNumeral('IV-7', key.Key(x.root().name), duration = newDuration))
    return expansion.flatten()


#replaces with 5-1
def derive3a(w, x, minor):
    # name = x.commonName
    # if (name != 'dominant seventh chord'):
    #     sys.stderr.write("derive3a: unable to derive non-dominant chord\n")
    replacement = stream.Stream()
    totalDur = w.duration.quarterLength + x.duration.quarterLength
    domDuration = w.duration
    if (minor):
        replacement.append(roman.RomanNumeral('v-7', key.Key(x.root().name), duration = domDuration))
    else:
        replacement.append(roman.RomanNumeral('V-7', key.Key(x.root().name), duration = domDuration))
    
    remainingDur = duration.Duration((totalDur - domDuration.quarterLength))
    replacement.append(chord.Chord(x, duration = remainingDur))
    return replacement.flatten()

# def derive3b(w, x):
#     name = x.commonName
#     # if (name != 'minor seventh chord'):
#     #     sys.stderr.write("derive3a: unable to derive non-minor-dominant chord\n")
#     #     return chord.Chord(x, duration = duration.Duration(x.duration.quarterLength + w.duration.quarterLength))
#     replacement = stream.Stream()
#     domDuration = w.duration
#     replacement.append(roman.RomanNumeral('V7', key.Key(x.root().name), duration = domDuration))
#     replacement.append(chord.Chord(x, duration = x.duration))
#     return replacement.flatten()


#tri-tone sub
def derive4(d, x):
    #Todo: check that d is V7 of x
    name = x.commonName
    if not(name == 'minor seventh chord' or name == 'minor triad' or name == 'dominant seventh chord' or name == 'major triad'):
        sys.stderr.write("derive4: Chord not recognized\n")
        return x
    replacement = stream.Stream()
    superTonDuration = d.duration
    quality = x.quality
    if (quality == 'minor'):
        replacement.append(roman.RomanNumeral('bii-7', key.Key(x.root().name), duration = superTonDuration))
    else:
        replacement.append(roman.RomanNumeral('bII-7', key.Key(x.root().name), duration = superTonDuration))
    replacement.append(x)
    return replacement.flatten()

def derive5(x):
    replacement = stream.Stream()
    replacement.append(chord.Chord(x, x.duration))
    replacement.append(roman.RomanNumeral('ii', key.Key(x.root().name), duration = x.duration))
    replacement.append(roman.RomanNumeral('iii', key.Key(x.root().name), duration = x.duration))
    return replacement.flatten()


def makeDominant(x):
    major_seventh_interval = interval.Interval("M7")
    major_seventh_note = major_seventh_interval.transposePitch(x.root())
    secondChord = chord.Chord(x, duration = x.duration)
    secondChord.add(major_seventh_note)
    return (secondChord)

def testDerive3Unequal():
    k = key.Key("C")
    full = duration.Duration(4.0)
    half = duration.Duration(1.0)
    derive3a(roman.RomanNumeral('I', k, duration = half), roman.RomanNumeral('I', k, duration = full), False).show()

    print("----------------")
    


def main():
    #testDerive3Unequal()
    k = key.Key('C')
    s = derive0(k)
    
    applyDerive3a(s)
    s = s.flatten()

    s = stream.tools.removeDuplicates(s)

    for i in range(5):
        applyDerive1(s)
        s = s.flatten()
        applyDerive3a(s)
        s = s.flatten()

            
    for el in s.recurse():
        print(el.root().name + " " + el.commonName + " " + str(el.duration.quarterLength) + " beats")



    

    #print names of chords
    # for el in s.recurse():
    #     print(el.root().name + " " + el.commonName + " " + str(el.duration.quarterLength) + " beats")

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
