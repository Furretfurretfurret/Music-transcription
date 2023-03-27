from music21 import converter
from pydub import AudioSegment
from music21 import audioSearch, midi, stream

import librosa
import mido
import numpy as np
import warnings
from math import floor, ceil
warnings.simplefilter(action='ignore', category=FutureWarning)


def mp3_to_midi(mp3_path):
    # Load audio file
    y, sr = librosa.load(mp3_path, sr=None, mono=True, offset=0.0, duration=None, res_type='kaiser_best', dtype=np.float32)

    # Extract pitches and timing from audio file
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitches = pitches.T
    magnitudes = magnitudes.T

    # Create MIDI file
    midi_file = mido.MidiFile()
    track = mido.MidiTrack()
    midi_file.tracks.append(track)

    # Add pitch and timing data to MIDI file
    ticks_per_beat = midi_file.ticks_per_beat
    magnitudes /= np.amax(magnitudes)
    pitches /= np.amax(pitches)
    for frame, frame_pitches in enumerate(pitches):
        time = librosa.frames_to_time(frame, sr=sr)
        for pitch, magnitude in zip(frame_pitches, magnitudes[frame]):
            if magnitude > 0:
                note_on = mido.Message('note_on', note=int(round(pitch)),
                                       velocity=int(127 * magnitude),
                                       time=int(time * ticks_per_beat))
                note_off = mido.Message('note_off', note=int(round(pitch)),
                                        velocity=0,
                                        time=int((time + 0.01) * ticks_per_beat))
                track.append(note_on)
                track.append(note_off)

    return midi_file

def midi_to_xml(midi_file, xml_path):
    # Load MIDI file
    print("Attempting to Parse")
    midi_stream = midi.translate.midiFilePathToStream("temp.midi")
    print("Finished Parsing")
    # Convert to MusicXML and save
    print("Attepting to write to MusicXML")
    midi_stream.write('musicxml', xml_path)
    print("Wrote to MusicXML")

audioFilePath = "S:\\CSCE 482\\Furret\\Server\\audioSamples\\"
fileName = "Joji-Glimpse of Us.mp3"
xmlFilePath = "S:\\CSCE 482\\Furret\\Server\\xmlCollection"

# midi_file = mp3_to_midi(audioFilePath + fileName)
midi_to_xml(None, xmlFilePath)
