from music21 import stream, note
import hashlib
import random

# 19 notas musicales para base 19
NOTAS_BASE_19_ORIGINAL = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 
                          'A#', 'C#', 'D#', 'F#', 'G#', 
                          'a', 'b', 'c', 'd', 'e', 'f', 'g']

LIMITE_CARACTERES = 50

def generar_reorganizacion(clave):
    """
    Genera una reorganización de las notas basada en la clave proporcionada.
    La misma clave siempre producirá la misma reorganización.
    """
    hash_clave = hashlib.sha256(clave.encode()).digest()
    
    #Esto si me lo dio chat porque no sabia como hacerlo # que viva copilot
    seed = int.from_bytes(hash_clave, byteorder='big') % (2**32)
    
    # Creamos una copia de las notas originales
    notas_reorganizadas = NOTAS_BASE_19_ORIGINAL.copy()

    random.seed(seed)
    random.shuffle(notas_reorganizadas)
    
    return notas_reorganizadas

def texto_a_melodia(texto, clave):
    """Convierte un mensaje en una melodía usando base 19 con una clave personalizada."""
    notas_base_19 = generar_reorganizacion(clave)
    
    ascii_values = [ord(c) for c in texto]  # Convertir cada carácter a su valor ASCII
    notas_melodia = []
    
    for val in ascii_values:
        notas = []
        while val > 0:
            notas.append(notas_base_19[val % 19])
            val //= 19
        while len(notas) < 2:  # Cada valor ASCII tiene al menos 2 notas
            notas.insert(0, notas_base_19[0])  # Se rellena con la primera nota de la lista reorganizada
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

def melodia_a_texto(notas, clave):
    """Convierte una secuencia de notas a texto original usando la clave proporcionada."""
    # Obtenemos la reorganización de notas basada en la clave
    notas_base_19 = generar_reorganizacion(clave)
    
    valores_base19 = []
    for n in notas:
        if n in notas_base_19:
            valores_base19.append(notas_base_19.index(n))
        else:
            print(f"Advertencia: La nota '{n}' no está en la lista de notas válidas con esta clave.")

    mensaje_recuperado = ""
    i = 0
    while i < len(valores_base19):
        # Intentamos formar caracteres ASCII válidos
        valor_ascii = 0
        max_digitos = min(4, len(valores_base19) - i)  # Limitamos a 4 dígitos máximo
        
        for j in range(max_digitos):
            valor_ascii = valor_ascii * 19 + valores_base19[i + j]
            if 32 <= valor_ascii <= 126:  # Rango de ASCII imprimible
                mensaje_recuperado += chr(valor_ascii)
                i += j + 1
                break
        else:
            # Si no encontramos un carácter ASCII válido, avanzamos un dígito
            i += 1

    return mensaje_recuperado

def mostrar_info_clave(clave):
    """Muestra información sobre la reorganización generada por la clave."""
    notas_reorganizadas = generar_reorganizacion(clave)
    print("\nInformación de la clave:")
    print(f"Clave: '{clave}'")
    print("Reorganización de notas:")
    for i, nota in enumerate(notas_reorganizadas):
        print(f"{i}: {nota}")
    print()

# Menú de acciones para el usuario
def menu_principal():
    print("\n===== CIFRADO MUSICAL CON CLAVE =====")
    print("1. Codificar mensaje")
    print("2. Decodificar melodía")
    print("3. Ver información de una clave")
    print("4. Salir")
    return input("Selecciona una opción (1-4): ").strip()

# Ejecución principal
if __name__ == "__main__":
    while True:
        opcion = menu_principal()
        
        if opcion == "1":
            mensaje = input(f"Ingresa el mensaje secreto (max {LIMITE_CARACTERES} caracteres): ").strip()
            
            if len(mensaje) > LIMITE_CARACTERES:
                print(f"Error: El mensaje es demasiado largo (max {LIMITE_CARACTERES} caracteres).")
            else:
                clave = input("Ingresa la clave secreta: ").strip()
                if not clave:
                    print("Error: La clave no puede estar vacía.")
                    continue
                    
                notas_melodia = texto_a_melodia(mensaje, clave)
                print("\nNotas generadas:")
                print(' '.join(notas_melodia))
                
                generar_archivo = input("¿Generar archivo MIDI? (s/n): ").strip().lower()
                if generar_archivo == 's':
                    nombre_archivo = input("Nombre del archivo MIDI (o Enter para 'melodia.mid'): ").strip()
                    if not nombre_archivo:
                        nombre_archivo = "melodia.mid"
                    generar_midi(notas_melodia, nombre_archivo)
        
        elif opcion == "2":
            notas_input = input("Ingresa la lista de notas separadas por espacio: ").strip().split()
            clave = input("Ingresa la clave secreta para decodificar: ").strip()
            
            if not clave:
                print("Error: La clave no puede estar vacía.")
                continue
                
            mensaje_decodificado = melodia_a_texto(notas_input, clave)
            print("\nMensaje decodificado:", mensaje_decodificado)
        
        elif opcion == "3":
            clave = input("Ingresa la clave para ver su información: ").strip()
            if not clave:
                print("Error: La clave no puede estar vacía.")
                continue
            mostrar_info_clave(clave)
        
        elif opcion == "4":
            print("¡Hasta pronto!")
            break
            
        else:
            print("Opción no válida. Por favor, selecciona una opción del 1 al 4.")