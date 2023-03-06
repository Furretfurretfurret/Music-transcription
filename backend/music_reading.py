import os
import subprocess
from music21 import *
import fluidsynth
import pygame
import tkinter as tk

# Music21 needs musescore installed
    # b = converter.parse(os.path.join(output_path, name_of_sheet))
    # b.show()

def scanningMusic(input_path, output_path):
    folderSheetMusic(output_path)
    command = ['oemer', input_path, '-o', output_path, '--save-cache']
    subprocess.run(command, check=True)
    

def folderSheetMusic(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

class AudioPlayer:
    def __init__(self, master, output_path, musicxml_file, midi_file):
        self.master = master
        master.title("Audio Player")

        # Create Play Button
        self.play_button = tk.Button(master, text="Play", command=lambda: self.play_audio(output_path, musicxml_file, midi_file))
        self.play_button.pack()

        # Create Pause Button
        self.pause_button = tk.Button(master, text="Pause", command=self.pause_audio)
        self.pause_button.pack()

        # Create Resume Button
        self.resume_button = tk.Button(master, text="Resume", command=self.resume_audio)
        self.resume_button.pack()

        # Create Stop Button
        self.stop_button = tk.Button(master, text="Stop", command=self.stop_audio)
        self.stop_button.pack()

        # Music21 needs musescore installed
        # b = converter.parse(os.path.join(output_path, name_of_sheet))
        # b.show()

        # Initialize pygame
        pygame.init()

        # Set up audio playback
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1.0)
        self.playing = False
        self.paused = False
    def play_audio(self, output_path, musicxml_file, midi_file):
        pygame.init()

        # Convert MusicXML to MIDI
        s = converter.parse(os.path.join(output_path, musicxml_file))
        mf = midi.translate.streamToMidiFile(s)
        mf.open(os.path.join(output_path, midi_file), 'wb')
        mf.write()
        mf.close()

        # Load and play the MIDI file with pygame
        pygame.mixer.music.load(os.path.join(output_path, midi_file))
        pygame.mixer.music.play()
        self.playing = True
        self.paused = False

        # while pygame.mixer.music.get_busy() == True:
        #     continue
    def pause_audio(self):
        if self.playing:
            pygame.mixer.music.pause()
            self.paused = True

    def resume_audio(self):
        if self.playing and self.paused:
            pygame.mixer.music.unpause()
            self.paused = False

    def stop_audio(self):
        if self.playing:
            pygame.mixer.music.stop()
            self.playing = False
            self.paused = False


def audioOutput(output_path, musicxml_file, midi_file):
    pygame.init()

    # Convert MusicXML to MIDI
    s = converter.parse(os.path.join(output_path, musicxml_file))
    mf = midi.translate.streamToMidiFile(s)
    mf.open(os.path.join(output_path, midi_file), 'wb')
    mf.write()
    mf.close()

    # Load and play the MIDI file with pygame
    pygame.mixer.music.load(os.path.join(output_path, midi_file))
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() == True:
        continue

def main():
    name_of_sheet = 'Glimpse_of_us_jpg-1.jpg'
    index = name_of_sheet.find('.', 2)
    name_of_sheet = name_of_sheet[0:index]

    musicxml_file = name_of_sheet + '.musicxml'
    midi_file = name_of_sheet + '.mid'
    jpg_file = name_of_sheet + '.jpg'

    input_path = os.path.join('..', 'sheets', jpg_file)
    output_path = os.path.join('..', 'model', name_of_sheet)

    # scanningMusic(input_path, output_path)
    # audioOutput(output_path, musicxml_file, midi_file)


    root = tk.Tk()
    audio_player = AudioPlayer(root, output_path, musicxml_file, midi_file)
    root.mainloop()

if __name__ == "__main__":
    main()