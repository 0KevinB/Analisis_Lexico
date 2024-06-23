# Definir las reglas del lenguaje
palabras_reservadas = {'if', 'else', 'while', 'for', 'return'}
operadores = {'+', '-', '*', '/', '==', '!=', '=', '&&', '||', '!'}
simbolos_agrupacion = {'(', ')', '{', '}', '[', ']'}
separadores = {',', ';'}

def es_palabra_reservada(cadena):
    return cadena in palabras_reservadas

def es_identificador(cadena):
    if cadena[0].isalpha() or cadena[0] == '_':
        for char in cadena:
            if not (char.isalnum() or char == '_'):
                return False
        return True
    return False

def es_numero(cadena):
    if cadena.isdigit():
        return True
    if '.' in cadena:
        partes = cadena.split('.')
        if len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
            return True
    return False

def es_operador(cadena):
    return cadena in operadores

def es_simbolo_agrupacion(cadena):
    return cadena in simbolos_agrupacion

def es_separador(cadena):
    return cadena in separadores

def es_comentario(cadena):
    return cadena.startswith('//') or (cadena.startswith('/*') and cadena.endswith('*/'))

def es_cadena_caracteres(cadena):
    return (cadena.startswith('"') and cadena.endswith('"')) or (cadena.startswith("'") and cadena.endswith("'"))

def identificar_tipo(cadena):
    if es_palabra_reservada(cadena):
        return 'palabra reservada'
    if es_identificador(cadena):
        return 'identificador'
    if es_numero(cadena):
        return 'numero'
    if es_operador(cadena):
        return 'operador'
    if es_simbolo_agrupacion(cadena):
        return 'simbolo de agrupacion'
    if es_separador(cadena):
        return 'separador'
    if es_comentario(cadena):
        return 'comentario'
    if es_cadena_caracteres(cadena):
        return 'cadena de caracteres'
    return 'desconocido'

def analizar_linea(linea):
    tokens = []  # Lista para almacenar los tokens encontrados
    i = 0  # Índice para recorrer la línea de texto
    
    # Bucle principal para recorrer cada carácter en la línea
    while i < len(linea):
        # Ignorar espacios en blanco, tabulaciones y nuevas líneas
        if linea[i] in {' ', '\t', '\n'}:
            i += 1
            continue
        
        # Detectar comentarios de línea
        if linea[i:i+2] == '//':
            tokens.append(linea[i:].strip())  # Agregar el resto de la línea como un comentario
            break  # Terminar el análisis de la línea
        
        # Detectar comentarios de bloque
        if linea[i:i+2] == '/*':
            end = linea.find('*/', i + 2)  # Buscar el final del comentario de bloque
            if end == -1:
                tokens.append(linea[i:].strip())  # Agregar el resto de la línea como un comentario
                break  # Terminar el análisis de la línea
            else:
                tokens.append(linea[i:end+2].strip())  # Agregar el comentario de bloque completo
                i = end + 2  # Continuar después del comentario de bloque
                continue
        
        # Detectar cadenas de caracteres (comillas simples o dobles)
        if linea[i] in {'"', "'"}:
            quote = linea[i]  # Guardar el tipo de comilla utilizada
            end = i + 1  # Inicializar índice para buscar el final de la cadena
            while end < len(linea) and linea[end] != quote:
                end += 1
            if end < len(linea):
                tokens.append(linea[i:end+1])  # Agregar la cadena completa como un token
                i = end + 1  # Continuar después de la cadena
            else:
                tokens.append(linea[i:])  # Agregar el resto de la línea si la cadena no se cierra
                break  # Terminar el análisis de la línea
        
        else:
            # Detectar otros tokens
            j = i
            while j < len(linea) and linea[j] not in {' ', '\t', '\n', '(', ')', '{', '}', '[', ']', ',', ';', '+', '-', '*', '/', '=', '!', '&', '|'}:
                j += 1
            if i == j:
                # Si `i` y `j` son iguales, significa que hemos encontrado un delimitador individual
                tokens.append(linea[i])  # Agregar el delimitador como un token
                i += 1  # Avanzar al siguiente carácter
            else:
                # Si `j` avanzó, significa que hemos encontrado un token
                tokens.append(linea[i:j])  # Agregar el token encontrado
                i = j  # Continuar después del token encontrado
    
    return tokens  # Devolver la lista de tokens encontrados

def analizar_archivo(archivo):
    with open(archivo, 'r') as file:
        lineas = file.readlines()

    resultados = []
    for linea in lineas:
        linea = linea.strip()  # Eliminar espacios en blanco alrededor
        if linea:  # Ignorar líneas vacías
            tokens = analizar_linea(linea)
            for token in tokens:
                tipo = identificar_tipo(token)
                resultados.append((token, tipo))
    
    return resultados

archivo = 'codigo2.txt' 
resultados = analizar_archivo(archivo)

for token, tipo in resultados:
    print(f'entra: {token}\ndevuelve: {tipo}\n')
