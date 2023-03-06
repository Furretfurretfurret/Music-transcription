# testing audio to midi conversion
# import librosa 
# audio_data, sample_rate = librosa.load('audio_file.wav')

# from librosa.core import piptrack
# pitch, magnitude = piptrack(audio_data, sr=sample_rate, fmin=50, fmax=2000)

from midiutil.MidiFile import MIDIFile
midi = MIDIFile(numTracks=1)
track = 0
time = 0
channel = 0
volume = 100
midi.addTrackName(track, time, "Track")
midi.addTempo(track, time, 120)
for i in range(len(pitch)):
    pitch_value = int(round(pitch[i]))
    if pitch_value != -1:
        time += 1
        midi.addNote(track, channel, pitch_value, time, 1, volume)
with open("output.mid", "wb") as output_file:
    midi.writeFile(output_file)