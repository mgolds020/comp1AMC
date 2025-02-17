#!/usr/bin/env python3
# Purpose: Generate harmonies using Jazz Chord Sequences Grammer
#
# 
# Author(s): Jake Kerrigan and Milo Goldstein
# Date: 02/10/26

import sys
from music21 import *
import math
import copy

#Useful Python functions (choice and choices) to randomly select something from
#a collection
from random import choice, choices 

#harmony generation

def derive0(k):
    s = stream.Part()
    d = duration.Duration(8.0)

    #test out derive 1


    s.append(chord.Chord(roman.RomanNumeral('I', k), duration = d))

    s.append(chord.Chord(roman.RomanNumeral('I7[b7]', k), duration = d))
    
    s.append(chord.Chord(roman.RomanNumeral('IV7[b7]', k), duration = d))

    s.append(chord.Chord(roman.RomanNumeral('I', k), duration = d))

    s.append(chord.Chord(roman.RomanNumeral('V7', k), duration = d))
    
    s.append(chord.Chord(roman.RomanNumeral('I', k), duration = d))

    return s
    


def isFith(chord1, chord2):
    major_seventh_interval = interval.Interval("p5")
    perfect_fith_note = major_seventh_interval.transposePitch(chord2.root())
    return chord1.root() == perfect_fith_note

def applyDerive1(s):

    iterationCounter = 0

    index = skewedIndexGenerator(len(s))
    chordToDerive = s[index]

    while(chordToDerive.duration.quarterLength < minDuration * 2):
        if(iterationCounter > len(s)):
            return
        
        index = skewedIndexGenerator(len(s))
        chordToDerive = s[index]
        iterationCounter += 1

    offset = chordToDerive.offset
    s.pop(index)
    s.insert(offset, derive1(chordToDerive))
    s = s.flatten()

def applyDerive2(s):
    iterationCounter = 0
    index = skewedIndexGenerator(len(s))
    chordToDerive = s[index]

    while(chordToDerive.duration.quarterLength < minDuration * 2):
        if(iterationCounter > len(s)):
            return
        
        index = skewedIndexGenerator(len(s))
        chordToDerive = s[index]

        iterationCounter += 1


        
    offset = chordToDerive.offset
    s.pop(index)
    s.insert(offset, derive2(chordToDerive))
    s = s.flatten()

def applyDerive3a(s):


    index = skewedIndexGenerator(len(s) - 1)
    chordToDerive = s[index]
    nextChordToDerive = s[(index + 1)]
        

    offset = chordToDerive.offset


    s.pop(index)
    s.pop(index)
    isMinor = choice(range(1))
    s.insert(offset, derive3a(chordToDerive, nextChordToDerive, False))
    s = s.flatten()


        
   



def applyDerive4(s):
    
    iterationCounter = 1

    index = skewedIndexGenerator(len(s) - 1)
    chordToDerive = s[index]
    nextChordToDerive = s[(index + 1)]
    
    

    triToneSubable = isFith(chordToDerive, nextChordToDerive)


    while(triToneSubable):

        if(iterationCounter > len(s)):
            return

        index = skewedIndexGenerator(len(s) - 1)
        chordToDerive = s[index]
        nextChordToDerive = s[index + 1]
        triToneSubable = isFith(chordToDerive, nextChordToDerive)
        iterationCounter += 1
    
    offset = chordToDerive.offset


    s.pop(index)
    s.pop(index)
    s.insert(offset, derive4(chordToDerive, nextChordToDerive))
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
    expansion.append(chord.Chord(roman.RomanNumeral('I-7', key.Key(diminutedChord.root().name)), duration = newDuration))
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
    expansion.append(chord.Chord(roman.RomanNumeral('IV-7', key.Key(x.root().name)), duration = newDuration))
    return expansion.flatten()


#replaces with 5-1
def derive3a(w, x, minor):

    replacement = stream.Stream()
    totalDur = w.duration.quarterLength + x.duration.quarterLength
    domDuration = w.duration
    if (minor):
        replacement.append(chord.Chord(roman.RomanNumeral('V-7', key.Key(x.root().name)), duration = domDuration))
    else:
        replacement.append(chord.Chord(roman.RomanNumeral('V7', key.Key(x.root().name)), duration = domDuration))
    
    replacement.append(chord.Chord(x, duration = x.duration))
    return replacement.flatten()


#tri-tone sub
def derive4(d, x):
    name = x.commonName
    if not(name == 'minor seventh chord' or name == 'minor triad' or name == 'dominant seventh chord' or name == 'major triad'):
        sys.stderr.write("derive4: Chord not recognized\n")
        return x
    replacement = stream.Stream()
    superTonDuration = d.duration
    quality = x.quality
    if (quality == 'minor'):
        replacement.append(chord.Chord(roman.RomanNumeral('bii-7', key.Key(x.root().name)), duration = superTonDuration))
    else:
        replacement.append(chord.Chord(roman.RomanNumeral('bII-7', key.Key(x.root().name)), duration = superTonDuration))
    replacement.append(x)
    return replacement.flatten()

def makeDominant(x):
    major_seventh_interval = interval.Interval("M7")
    major_seventh_note = major_seventh_interval.transposePitch(x.root())
    secondChord = chord.Chord(x, duration = x.duration)
    secondChord.add(major_seventh_note)
    return (secondChord)


# generates a 0-indexed index based on length parameter that is random but
# tends to be a larger index

def skewedIndexGenerator(length):
    intialIndex  = math.ceil(length / 2)

    index = intialIndex + choice(range(int(length / 2)))

    #50% chance to normalize index by getting by subtracting 

    if(choice(range(1))):
        index -= choice(range(int(length / 2)))
    return index



#testing functions:


def testDerive3Unequal():
    k = key.Key("C")

    derivation1 = derive1(chord.Chord(roman.RomanNumeral('I', k), duration = duration.Duration(8.0)))
    

    applyDerive3a(derivation1)

    derivation1.flatten().show()

    derivation1.show('text')


#melody generation

def retrograde(sequence):
    sequence.reverse()
    return sequence

def inversion(sequence):
    newList = []
    for i in range(len(sequence) - 1):
        newList.append((4 - sequence[i + 1]) - sequence[i])
    for i in range(len(newList)):
        sequence[i + 1] = ((sequence[i] + newList[i]) % 5)
    return sequence

def retrogradeInversion(sequence):
    return inversion(retrograde(sequence))

def transposition(sequence, number):
    for i in range(len(sequence)):
        sequence[i] = ((sequence[i] + number) % 5)
    return sequence


def makeMinBlues(key):
    return [pitch.Pitch(key.tonic.midi),
            pitch.Pitch(key.tonic.midi + 2),
            pitch.Pitch(key.tonic.midi + 3),
            pitch.Pitch(key.tonic.midi + 5),
            pitch.Pitch(key.tonic.midi + 6),
            pitch.Pitch(key.tonic.midi + 7),
            pitch.Pitch(key.tonic.midi + 10)
            ]


def applyRhythms(rhythmSequence, key):
    bluesScaleArray = makeMinBlues(key)
    noteStream = stream.Stream()
    for index in rhythmSequence:
        if   (index == 0):
            noteStream.append(note.Note(choice(bluesScaleArray), duration = duration.Duration(1.0)))
        elif (index == 1):
            noteStream.append(note.Rest(1.0))
        elif (index == 2):
            noteStream.append(note.Note(choice(bluesScaleArray), duration = duration.Duration(0.5)))
            noteStream.append(note.Note(choice(bluesScaleArray), duration = duration.Duration(0.5)))
        elif (index == 3):
            noteStream.append(note.Note(choice(bluesScaleArray), duration = duration.Duration(0.5)))
            noteStream.append(note.Rest(0.5))
        else:
            noteStream.append(note.Rest(0.5))
            noteStream.append(note.Note(choice(bluesScaleArray), duration = duration.Duration(0.5)))
    
    return noteStream

def makeNoteSequence(key):
    rhythmsSection1n2 = choices(range(5),  k=16)
    rhythmsSection3 = choices(range(5),  k=16)
    functions = [retrograde, inversion, retrogradeInversion, transposition]
    for i in range(4):
        transformation = choice(functions)
        if (transformation == transposition):
            randAdjustment = choice(range(5))
            transformation(rhythmsSection1n2, randAdjustment)
            transformation(rhythmsSection3, randAdjustment)
        else:
            transformation(rhythmsSection1n2)
            transformation(rhythmsSection3)
    streamSection1n2 = applyRhythms(rhythmsSection1n2, key)
    streamSection3 = applyRhythms(rhythmsSection3, key)
    duplicatedStream = stream.Part()
    duplicatedStream.insert(0, streamSection1n2)
    duplicatedStream.insert(16, copy.deepcopy(streamSection1n2))
    duplicatedStream.insert(32, streamSection3)
    return duplicatedStream


        

    



#testing code:
    # rhythms = choices(range(5),  k=16)
    # print(rhythms)
    # retrograde(rhythms)
    # print(rhythms)
    # retrograde(rhythms)
    # print(rhythms)
    # inversion(rhythms)
    # print(rhythms)
    # transposition(rhythms, 2)
    # print(rhythms)






def main():
    # testDerive3Unequal()
    print("Welcome to Blues Harmony Generator!")
    print("This program uses a grammer based system to perfrom derivations on a standard 12 bar blues!")
    k = key.Key(input("Please enter the key you would like the blues to be in: (e.x C) "))
    derivations = int(input("Please enter how many rounds of derivations you would like to perform: (e.x 3) "))
    global minDuration
    minDuration = int(input("Please enter the minimum chord length duration in quarter notes: (e.x 2) "))
    

    s = derive0(k)
    s = s.flatten()


    for i in range(derivations):
        applyDerive1(s)
        s = s.flatten()
        
        applyDerive3a(s)
        s = s.flatten()
        
        applyDerive4(s)
        s = s.flatten()
    
    melodyStream = makeNoteSequence(k)
    melodyStream.insert(48, copy.deepcopy(melodyStream))
    melodyStream = melodyStream.flatten()

    harmonyStream = s
    harmonyStream.insert(48, copy.deepcopy(s))
    harmonyStream = harmonyStream.flatten()

    
    harmonyStream.insert(0, instrument.ElectricPiano())
    

    finalStream = stream.Score()
    finalStream.insert(0, melodyStream)
    finalStream.insert(0, harmonyStream)
 

    finalStream.insert(0, metadata.Metadata())
    finalStream.metadata.title = '12 Bar Blues (2 times)'
    finalStream.metadata.composer = 'Jake Kerrigan and Milo Goldstein'





    
    if ("-m" in sys.argv):
        finalStream.show('midi')
    elif ("-s" in sys.argv):
        finalStream.show()
    else:
        finalStream.show('text')

if __name__ == "__main__":
    main()
