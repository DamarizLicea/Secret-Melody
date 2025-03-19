from music21 import stream, note, midi

# 19 notas musicales para base 19
NOTAS_BASE_19 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 
                 'A#', 'C#', 'D#', 'F#', 'G#', 
                 'a', 'b', 'c', 'd', 'e', 'f', 'g']

LIMITE_CARACTERES = 50 

def texto_a_melodia(texto):
    """Convierte un mensaje en una melodía usando base 19."""
    ascii_values = [ord(c) for c in texto]  # Obtener valores ASCII
    notas_melodia = []
    
    for val in ascii_values:
        notas = []
        while val > 0:
            notas.append(NOTAS_BASE_19[val % 19])
            val //= 19
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
        for v in valores_base19[:]:
            valor_ascii = valor_ascii * 19 + v
            valores_base19.pop(0)
            if valor_ascii >= 0: 
                mensaje_recuperado += chr(valor_ascii)
                break

    return mensaje_recuperado

# Menu de acciones
opcion = input("¿Quieres (1) Codificar o (2) Decodificar?: ")

if opcion == "1":
    mensaje = input(f"Ingresa el mensaje secreto (máx {LIMITE_CARACTERES} caracteres): ").strip()
    
    if len(mensaje) > LIMITE_CARACTERES:
        print(f"Error: El mensaje es demasiado largo (máx {LIMITE_CARACTERES} caracteres).")
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
