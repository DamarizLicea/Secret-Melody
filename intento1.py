from music21 import stream, note

# 19 notas musicales para base 19
NOTAS_BASE_19 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 
                 'A#', 'C#', 'D#', 'F#', 'G#', 
                 'a', 'b', 'c', 'd', 'e', 'f', 'g']

LIMITE_CARACTERES = 50

def texto_a_melodia(texto):
    """Convierte un mensaje en una melodía usando base 19."""
    ascii_values = [ord(c) for c in texto]  # Convertir cada carácter a su valor ASCII
    notas_melodia = []
    
    for val in ascii_values:
        notas = []
        while val > 0:
            notas.append(NOTAS_BASE_19[val % 19])
            val //= 19
        while len(notas) < 2:  # Cada valor ASCII tiene al menos 2 notas
            notas.insert(0, NOTAS_BASE_19[0])  # SINO, se rellena con la nota 'A'
        notas.reverse()
        notas_melodia.extend(notas)
    
    return notas_melodia

def generar_midi(notas, nombre_archivo="melodia.mid"):
    """Crea un archivo MIDI con las notas generadas."""
    melody = stream.Stream()
    for n in notas:
        melody.append(note.Note(n, quarterLength=1))  # Duración de 1 negra
    melody.write('midi', fp=nombre_archivo)
    print(f"Archivo MIDI generado: {nombre_archivo}")

def melodia_a_texto(notas):
    """Convierte una secuencia de notas a texto original."""
    valores_base19 = []
    for n in notas:
        if n in NOTAS_BASE_19:
            valores_base19.append(NOTAS_BASE_19.index(n))

    mensaje_recuperado = ""
    while valores_base19:
        valor_ascii = 0
        while valores_base19:  
            valor_ascii = valor_ascii * 19 + valores_base19.pop(0)
            if 32 <= valor_ascii <= 126:  # Rango de ASCII
                mensaje_recuperado += chr(valor_ascii)
                break

    return mensaje_recuperado

# Menú de acciones para el usuario
opcion = input("¿Quieres (1) Codificar o (2) Decodificar?: ")

if opcion == "1":
    mensaje = input(f"Ingresa el mensaje secreto (max {LIMITE_CARACTERES} caracteres): ").strip()
    
    if len(mensaje) > LIMITE_CARACTERES:
        print(f"Error: El mensaje es demasiado largo (max {LIMITE_CARACTERES} caracteres).")
    else:
        notas_melodia = texto_a_melodia(mensaje)
        print("Notas generadas:", notas_melodia)
        generar_midi(notas_melodia)

elif opcion == "2":
    notas_input = input("Ingresa la lista de notas separadas por espacio: ").strip().split()
    mensaje_decodificado = melodia_a_texto(notas_input)
    print("Mensaje decodificado:", mensaje_decodificado)

else:
    print("Opción no válida.")
