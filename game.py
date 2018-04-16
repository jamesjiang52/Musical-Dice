"""
Generates 16-measure waltzes based on Mozart's "Musical Table", a collection
of 176 measures. Measures are selected according to the rules of Mozart
himself.
"""

import time
from numpy.random import randint
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq
import pygame as pg


def get_measures():
    """
    The text file holds note data. Each line is in the form

    <note> <beat of actuation> <note duration>

    . For example,

    C3 6 2

    represents holding C3 for two beats, starting on beat 6.

    This function reads the text file and separates the notes into measures,
    each 3 beats long.
    """
    notes = [line.rstrip("\n").split(" ") for line in open("notes.txt")]

    measures = []
    current = []
    last_note = notes[-1]
    last_multiple = 0

    for note in notes:
        if (float(note[1]) % 3 == 0) and (float(note[1])//3 != last_multiple):
            last_multiple = float(note[1])//3
            measures.append(current)
            current = []
            current.append([note[0], float(note[1]), float(note[2])])
        else:
            current.append([note[0], float(note[1]), float(note[2])])
        if note == last_note:
            measures.append(current)

    return(measures)


def roll():
    """
    Simulates a roll of two dice and returns the total.
    """
    dice_1 = randint(1, 7)
    dice_2 = randint(1, 7)
    return(dice_1 + dice_2)


def measures_to_notes(measures):
    """
    measures: List[List[List[str, float, float]]]
         -> List[List[str, float, float]]

    Breaks up a list of measures of notes into a list of notes.
    """
    notes = []
    for i in range(len(measures)):
        notes.extend(measures[i])
    return(notes)


def note_to_index(note_str):
    """
    note_str: str -> int

    Returns the integer value of the note in note_str, given as an index in
    the list below.
    """
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    return(notes.index(note_str))


def create_song(song_notes, tempo):
    """
    song_notes: List[List[str, float, float]], tempo: int -> None

    Creates a MIDI file with notes given in song_notes and saves it at
    tmp/song.mid.
    """
    notes = []
    beat = 0

    while beat < 48:
        chord = []
        for song_note in song_notes:
            if song_note[1] == beat:
                if beat == 47:  # make last note longer
                    dur = 0.5
                else:
                    dur = song_note[2]/4
                note = Note(
                    value=note_to_index(song_note[0][:-1]),
                    octave=int(song_note[0][-1]) + 1,
                    dur=dur)
                chord.append(note)
        if chord != []:  # beat isn't a rest
            notes.append([NoteSeq(chord), beat])
        beat += 0.5

    midi = Midi(tempo=tempo)
    for note in notes:
        midi.seq_chords([note[0]], time=note[1])

    midi.write("tmp/song.mid")


def play_song(tempo):
    """
    Plays the created MIDI file located at tmp/song.mid.
    """
    pg.init()
    pg.mixer.music.load("tmp/song.mid")
    pg.mixer.music.play()
    time.sleep(48*60/tempo)


def main():
    """
    Simulates 16 dice rolls and makes the appropriate measure selections.
    Plays the created waltz afterwards.
    """
    song = []
    measures = get_measures()
    measure_selections = [
        [96, 32, 69, 40, 148, 104, 152, 119, 98, 3, 54],
        [22, 6, 95, 17, 74, 157, 60, 84, 142, 87, 130],
        [141, 128, 158, 113, 163, 27, 171, 114, 42, 165, 10],
        [41, 63, 13, 85, 45, 167, 53, 50, 156, 61, 103],
        [105, 146, 153, 161, 80, 154, 99, 140, 75, 135, 28],
        [122, 46, 55, 2, 97, 68, 133, 86, 129, 47, 37],
        [11, 134, 110, 159, 36, 118, 21, 169, 62, 147, 106],
        [30, 81, 24, 100, 107, 91, 127, 94, 123, 33, 5],
        [70, 117, 66, 90, 25, 138, 16, 120, 65, 102, 35],
        [121, 39, 136, 176, 143, 71, 155, 88, 77, 4, 20],
        [26, 126, 15, 7, 64, 150, 57, 48, 19, 31, 108],
        [9, 56, 132, 34, 125, 29, 175, 166, 82, 164, 92],
        [112, 174, 73, 67, 76, 101, 43, 51, 137, 144, 12],
        [49, 18, 58, 160, 136, 162, 168, 115, 38, 59, 124],
        [109, 116, 145, 52, 1, 23, 89, 72, 149, 173, 44],
        [14, 83, 79, 170, 93, 151, 172, 111, 8, 78, 131]]

    for i in range(16):
        roll_ = roll()
        measure_selection = measures[measure_selections[i][roll_ - 2] - 1][:]
        offset = measure_selection[0][1] - 3*i
        for j in range(len(measure_selection)):
            measure_selection[j][1] -= offset
        song.append(measure_selection)

    tempo = 120
    create_song(measures_to_notes(song), tempo)
    play_song(tempo)


if __name__ == "__main__":
    main()
