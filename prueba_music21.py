import music21
import os
from music21 import stream, note, midi

# Esto solo es una prueba para comprobar que music21 está instalado correctamente

# Crear una secuencia de notas (escala de Do mayor)
melody = stream.Stream()
notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']

for pitch in notes:
    melody.append(note.Note(pitch))

# Guardar la melodía en un archivo MIDI
midi_file = "test_scale.mid"
melody.write('midi', fp=midi_file)

print(f"Archivo MIDI generado: {midi_file}")


nota = note.Note('C4')
os.system("test_scale.mid")
nota.show()
nota.show('midi')
