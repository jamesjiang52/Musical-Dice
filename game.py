"""
Generates 16-measure waltzes based on Mozart's "Musical Table", a collection
of 176 measures. Measures are selected according to the rules of Mozart
himself.
"""

import numpy as np
import simpleaudio as sa
import time


def get_measures():
    """
    The text file holds note data. Each line is in the form

    <note> <beat of actuation> <beat duration>

    . For example,

    C3 6 2

    represents holding C3 for two beats, starting on beat 6.

    This function reads the text file and separates the notes into measures,
    each 3 beats long.
    """
    notes = [line.rstrip("\n").split(" ") for line in open("original.txt")]

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
    dice_1 = np.random.randint(1, 7)
    dice_2 = np.random.randint(1, 7)
    return(dice_1 + dice_2)


def play_song(song_measures, tempo):
    """
    song_measures: List[List[List[str, float, float]]], tempo: int -> None

    Plays the song, assuming that the notes are separated into measures. The
    tempo (beats/min) changes the speed of playback. At tempo=120, playback
    takes around 24 seconds (48 beats).
    """
    A3 = sa.WaveObject.from_wave_file("notes_audio/A3.wav")
    A4 = sa.WaveObject.from_wave_file("notes_audio/A4.wav")
    A5 = sa.WaveObject.from_wave_file("notes_audio/A5.wav")
    B2 = sa.WaveObject.from_wave_file("notes_audio/B2.wav")
    B3 = sa.WaveObject.from_wave_file("notes_audio/B3.wav")
    B4 = sa.WaveObject.from_wave_file("notes_audio/B4.wav")
    B5 = sa.WaveObject.from_wave_file("notes_audio/B5.wav")
    C_s_3 = sa.WaveObject.from_wave_file("notes_audio/C#3.wav")
    C_s_5 = sa.WaveObject.from_wave_file("notes_audio/C#5.wav")
    C2 = sa.WaveObject.from_wave_file("notes_audio/C2.wav")
    C3 = sa.WaveObject.from_wave_file("notes_audio/C3.wav")
    C4 = sa.WaveObject.from_wave_file("notes_audio/C4.wav")
    C5 = sa.WaveObject.from_wave_file("notes_audio/C5.wav")
    C6 = sa.WaveObject.from_wave_file("notes_audio/C6.wav")
    D2 = sa.WaveObject.from_wave_file("notes_audio/D2.wav")
    D3 = sa.WaveObject.from_wave_file("notes_audio/D3.wav")
    D4 = sa.WaveObject.from_wave_file("notes_audio/D4.wav")
    D5 = sa.WaveObject.from_wave_file("notes_audio/D5.wav")
    D6 = sa.WaveObject.from_wave_file("notes_audio/D6.wav")
    E3 = sa.WaveObject.from_wave_file("notes_audio/E3.wav")
    E4 = sa.WaveObject.from_wave_file("notes_audio/E4.wav")
    E5 = sa.WaveObject.from_wave_file("notes_audio/E5.wav")
    F_s_3 = sa.WaveObject.from_wave_file("notes_audio/F#3.wav")
    F_s_4 = sa.WaveObject.from_wave_file("notes_audio/F#4.wav")
    F_s_5 = sa.WaveObject.from_wave_file("notes_audio/F#5.wav")
    F3 = sa.WaveObject.from_wave_file("notes_audio/F3.wav")
    F5 = sa.WaveObject.from_wave_file("notes_audio/F5.wav")
    G2 = sa.WaveObject.from_wave_file("notes_audio/G2.wav")
    G3 = sa.WaveObject.from_wave_file("notes_audio/G3.wav")
    G4 = sa.WaveObject.from_wave_file("notes_audio/G4.wav")
    G5 = sa.WaveObject.from_wave_file("notes_audio/G5.wav")

    notes = {
        "A3": A3, "A4": A4, "A5": A5, "B2": B2, "B3": B3, "B4": B4, "B5": B5,
        "C#3": C_s_3, "C#5": C_s_5, "C2": C2, "C3": C3, "C4": C4, "C5": C5,
        "C6": C6, "D2": D2, "D3": D3, "D4": D4, "D5": D5, "D6": D6, "E3": E3,
        "E4": E4, "E5": E5, "F#3": F_s_3, "F#4": F_s_4, "F#5": F_s_5, "F3": F3,
        "F5": F5, "G2": G2, "G3": G3, "G4": G4, "G5": G5}

    for i in range(16):
        start = time.time()
        while (time.time() - start) <= 3*60/tempo:
            for j in range(len(song_measures[i])):
                note = song_measures[i][j]
                if note[1] != "done":
                    if (note[1] - 3*i) <= (time.time() - start)*tempo/60:
                        notes[note[0]].play()
                        song_measures[i][j][1] = "done"


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

    play_song(song, 120)


if __name__ == "__main__":
    main()
