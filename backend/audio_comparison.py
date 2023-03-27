from music21 import *
import librosa

# Load MusicXML and audio files
mx_file = converter.parse('Glimpse_of_us_jpg-1.musicxml')
audio_file_path = 'Joji-Glimpse of Us.mp3'
y, sr = librosa.load(audio_file_path)

# Extract notes and beats from MusicXML and audio files
mx_notes = mx_file.flat.notes
mx_beats = mx_file.flat.getElementsByClass('Measure').stream().getElementsByClass('Beat')
audio_beats, _ = librosa.beat.beat_track(y=y, sr=sr)
audio_notes = librosa.onset.onset_detect(y=y, sr=sr)

# Define fault tolerances (in seconds) for note and beat alignment
note_tolerance = 0.1
beat_tolerance = 0.1

# Define feature comparisons
def compare_pitch(note, pitch):
    return note.pitch.frequency == pitch

def compare_duration(note, duration):
    return abs(note.duration.quarterLength - duration) < note_tolerance

def compare_onset(note, onset):
    return abs(note.offset - onset) < note_tolerance

def compare_beat(note, beat):
    return abs(mx_beats.index(note.beat) - beat) < beat_tolerance

def compare_velocity(note, velocity):
    return abs(note.volume.velocity - velocity) < 10

def compare_timbre(note, chroma):
    chroma_mx = mx_file.chordify().flat.getElementsByClass('Chord')[0].pitches.chroma
    chroma_audio = librosa.feature.chroma_cqt(y=y, sr=sr)[note.onset:note.offset]
    return abs(chroma_mx - chroma_audio).mean() < 0.2

def compare_rhythm(note, rhythm):
    onset_in_beats = mx_beats.index(note.beat) + note.beatOffset
    mx_beat_duration = mx_beats[onset_in_beats].duration.quarterLength
    audio_beat_duration = librosa.samples_to_time(librosa.onset.onset_to_frames(audio_notes[onset_in_beats], sr=sr), sr=sr)
    return abs(mx_beat_duration - audio_beat_duration) < beat_tolerance

# Compare each note and provide feedback
for i, note in enumerate(mx_notes):
    # Find corresponding note in audio file
    note_onset = note.offset
    note_offset = note.offset + note.duration.quarterLength
    audio_note_onset = librosa.frames_to_time(librosa.onset.onset_to_frames(y, sr=sr)[audio_note_index], sr=sr)
    audio_note_index = None
    for j in range(len(audio_notes)):
        if librosa.frames_to_time(librosa.onset.onset_to_frames(y, sr=sr)[j], sr=sr) >= note_onset and librosa.frames_to_time(librosa.onset.onset_to_frames(y, sr=sr)[j], sr=sr) <= note_offset:
            audio_note_index = j
            break
    if audio_note_index is None:
        print('Could not find note {} in audio file'.format(i))
        continue
    
    # Find audio note offset
    audio_note_offset = librosa.frames_to_time(librosa.time_to_frames(audio_note_onset, sr=sr) + len(librosa.onset.onset_to_frames(y, sr=sr)[audio_note_index]), sr=sr)
    
    # Compare note features
    if compare_pitch(note, librosa.midi_to_hz(librosa.hz_to_midi(y[librosa.time_to_samples(audio_note_onset):librosa.time_to_samples(audio_note_offset)]).mean())):
        print('Note {} pitch matches'.format(i))
    else:
        print('Note {} pitch does not match'.format(i))
        
    if compare_duration(note, librosa.samples_to_time(librosa.frames_to_samples(librosa.onset.onset_to_frames(y[librosa.time_to_samples(audio_note_onset):librosa.time_to_samples(audio_note_offset)], sr=sr), sr=sr))):
        print('Note {} duration matches'.format(i))
    else:
        print('Note {} duration does not match'.format(i))
        
    if compare_onset(note, audio_note_onset):
        print('Note {} onset matches'.format(i))
    else:
        print('Note {} onset does not match'.format(i))
        
    if compare_beat(note, audio_beats[audio_note_index]):
        print('Note {} beat matches'.format(i))
    else:
        print('Note {} beat does not match'.format(i))
        
    if compare_velocity(note, librosa.amplitude_to_db(y[librosa.time_to_samples(audio_note_onset):librosa.time_to_samples(audio_note_offset)]).mean()):
        print('Note {} velocity matches'.format(i))
    else:
        print('Note {} velocity does not match'.format(i))
        
    if compare_timbre(note, librosa.feature.chroma_cqt(y[librosa.time_to_samples(audio_note_onset):librosa.time_to_samples(audio_note_offset)], sr=sr).mean(axis=1)):
        print('Note {} timbre matches'.format(i))
    else:
        print('Note {} timbre does not match'.format(i))
        
    if compare_rhythm(note, librosa.samples_to_time(librosa.frames_to_samples(librosa.onset.onset_to_frames(y[librosa.time_to_samples(audio_note_onset):librosa.time_to_samples(audio_note_offset)], sr=sr), sr=sr))):
        print('Note {} rhythm matches'.format(i))
    else:
        print('Note {} rhythm does not match'.format(i))


