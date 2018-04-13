import numpy as np
import pyaudio
import wave
import time


def get_measures():
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
    dice_1 = np.random.randint(1, 7)
    dice_2 = np.random.randint(1, 7)
    return(dice_1 + dice_2)


def measures_to_notes(song_measures):
    notes = []
    for i in range(len(song_measures)):
        for j in range(len(song_measures[i])):
            notes.append(song_measures[i][j])
    return(notes)


def play_note(note_str, length, tempo, p_class, stream):
    chunk_size = 1024
    note_audio = wave.open("notes_audio/" + note_str + ".wav", "rb")

    data = note_audio.readframes(chunk_size)
    start = time.time()

    while (len(data) > 0) and (tempo/60*(time.time() - start) < length):
        stream.write(data)
        data = note_audio.readframes(chunk_size)


def play_song(song_notes, tempo):
    p = pyaudio.PyAudio()

    stream = p.open(
        format=p.get_format_from_width(2), channels=2, rate=11025, output=True)

    start = time.time()
    while True:
        for i in range(len(song_notes)):
            note = song_notes[i]
            if note[1] != "done":
                if note[1] >= (time.time() - start)*60/tempo:
                    play_note(note[0], note[2], tempo, p, stream)
                    song_notes[i][1] = "done"

    stream.stop_stream()
    stream.close()
    p.terminate()


def main():
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

    play_song(measures_to_notes(song), 120)


if __name__ == "__main__":
    main()
