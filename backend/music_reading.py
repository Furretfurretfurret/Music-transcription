import os
import subprocess
from music21 import *
import fluidsynth
import pygame

# Music21 needs musescore installed
    # b = converter.parse(os.path.join(output_path, name_of_sheet))
    # b.show()

def scanningMusic(input_path, output_path):
    command = ['oemer', input_path, '-o', output_path, '--save-cache']
    subprocess.run(command, check=True)
    

def folderSheetMusic(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

def main():
    name_of_sheet = 'Glimpse_of_us_jpg-1.jpg'
    input_path = os.path.join('..', 'sheets', name_of_sheet)
    output_path = os.path.join('..', 'xmls', name_of_sheet)

    index = output_path.find('.', 2)
    output_path = output_path[0: index] 

    # folderSheetMusic(output_path)
    # scanningMusic(input_path, output_path)

    index = name_of_sheet.find('.', 2)
    name_of_sheet = name_of_sheet[0:index]
    musicxml = name_of_sheet + '.musicxml'
    midi_file = name_of_sheet + '.mid'

    pygame.init()

    # Convert MusicXML to MIDI
    s = converter.parse(os.path.join(output_path, musicxml))
    mf = midi.translate.streamToMidiFile(s)
    mf.open(os.path.join(output_path, midi_file), 'wb')
    mf.write()
    mf.close()

    # Load and play the MIDI file with pygame
    pygame.mixer.music.load(os.path.join(output_path, midi_file))
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() == True:
        continue

if __name__ == "__main__":
    main()