import librosa
from music21 import converter, midi, stream

# Load audio file
audio_data, audio_sr = librosa.load('Joji - Glimpse of Us.mp3')

# Load MIDI file
midi_data = midi.MidiFile()
midi_data.open('Glimpse_of_us_jpg-1.mid')
midi_data.read()
midi_data.close()
midi_stream = converter.parse('Glimpse_of_us_jpg-1.mid')

# Resample audio data to match MIDI sample rate
audio_data_resampled = librosa.resample(audio_data, audio_sr, midi_data.ticksPerQuarterNote)

# Get MIDI notes from MIDI file
midi_notes = []
for note in midi_stream.flat.notes:
    if note.isNote:
        midi_notes.append(note)

# Get onsets and pitches from audio data
audio_onsets, audio_pitches = librosa.onset.onset_detect(audio_data_resampled, sr=midi_data.ticksPerQuarterNote, units='time')

# Compare MIDI notes to audio onsets and pitches
accuracy_count = 0
for midi_note in midi_notes:
    for i in range(len(audio_onsets)):
        if abs(audio_onsets[i] - midi_note.offset) <= midi_data.ticksToSeconds(midi_data.resolution):
            if librosa.hz_to_midi(audio_pitches[i]) == midi_note.pitch.midi:
                accuracy_count += 1
                break

# Calculate accuracy percentage
accuracy_percentage = (accuracy_count / len(midi_notes)) * 100
print(f"Accuracy: {accuracy_percentage}%")