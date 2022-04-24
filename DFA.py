import sys
import os.path


# Simbolos de operadores. Se excluyen resta y
# división debido a su doble significado
SYMBOLS = {
    "=" : "Asignación",
    "+ ": "Suma",
    "*" : "Multiplicación",
    "^" : "Potencia",
    "(" : "Paréntesis que abre",
    ")" : "Paréntesis que cierra"
}

NUM_ESPACIOS = 40


"""Recibe un archivo de texto con tokens y manda a procesarlos
linea por linea para imprimir su tipo.
"""
def lexerAritmetico(nombre_archivo):

    # Abrir archivo de entrada
    inputFile = open(nombre_archivo)

    # Limpiar archivo de salida
    open('output.txt', 'w').close()

    # Abrir archivo
    outputFile = open("output.txt", 'a', encoding='utf-8')

    # Imprimir nombres de las columnas con NUM_ESPACIOS de separación
    print('Token' + (' ' * (NUM_ESPACIOS - len('Token'))) + 'Tipo', file=outputFile)

    # Procesar cada linea del archivo de entrada
    for line in inputFile.readlines():
        processLine(line, inputFile, outputFile)
    
    # Cerrar archivos
    outputFile.close()
    inputFile.close()


"""Procesa una línea para identificar los tokens que se encuentran en esa línea.
El código se basa en Autómata Finito Determinista. 
"""
def processLine(line, inputFile, outputFile):

    unfinishedToken = []
    state = 'inicial'

    for token in line:

        if state == 'inicial':
            if token.isalpha():
                state = 'variable'
            elif token.isnumeric():
                state = 'entero'
            elif token == '-':
                state = 'resta'
            elif token == '/':
                state = 'division'
            elif isOperand(token):
                state = 'operador'
            elif token == '.':
                state = 'real'
            elif token in '_':
                error_sintaxis(inputFile, outputFile)
            elif token != ' ' and token != '\n':
                error_sintaxis(inputFile, outputFile)

            if token != ' ' and token != '\n':
                unfinishedToken.append(token)


        elif state == 'variable':
            if token.isalpha() or isInteger(token) or token == '_':
                state = 'variable'
            elif token == '-':
                clearTokensList(unfinishedToken, outputFile)
                state = 'resta'
            elif token == '/':
                clearTokensList(unfinishedToken, outputFile)
                state = 'division'
            elif isOperand(token):
                clearTokensList(unfinishedToken, outputFile)
                state = 'operador'
            elif token in '.':
                error_sintaxis(inputFile, outputFile)
            elif token == ' ':
                clearTokensList(unfinishedToken, outputFile)
                state = 'inicial'
            elif token != ' ' and token != '\n':
                error_sintaxis(inputFile, outputFile)

            if token != ' ' and token != '\n':
                unfinishedToken.append(token)


        elif state == 'entero':

            if token.isalpha():
                clearTokensList(unfinishedToken, outputFile)
                state = 'variable'
            elif isInteger(token):
                state = 'entero'
            elif token == '-':
                clearTokensList(unfinishedToken, outputFile)
                state = 'resta'
            elif token == '.':
                state = 'real'
            elif token == '/':
                clearTokensList(unfinishedToken, outputFile)
                state = 'division'
            elif isOperand(token):
                clearTokensList(unfinishedToken, outputFile)
                state = 'operador'
            elif token == ' ':
                clearTokensList(unfinishedToken, outputFile)
                state = 'inicial'
            elif token == '_':
                error_sintaxis(inputFile, outputFile)
            elif token != ' ' and token != '\n':
                error_sintaxis(inputFile, outputFile)

            if token != ' ' and token != '\n':
                unfinishedToken.append(token)


        elif state == 'operador':
            clearTokensList(unfinishedToken, outputFile)
            
            if token.isalpha():
                state = 'variable'
            elif token.isnumeric():
                state = 'entero'
            elif token == '-':
                state = 'resta'
            elif token == '/':
                state = 'division'
            elif isOperand(token):
                state = 'operador'
            elif token in '._':
                error_sintaxis(inputFile, outputFile)
            elif token != ' ' and token != '\n':
                error_sintaxis(inputFile, outputFile)

            if token != ' ' and token != '\n':
                unfinishedToken.append(token)


        elif state == 'division':
            if token == '/':
                state = 'comentario'
            else:
                clearTokensList(unfinishedToken, outputFile)
                
                if token.isalpha():
                    state = 'variable'
                elif token.isnumeric():
                    state = 'entero'
                elif token == '-':
                    state = 'resta'
                elif isOperand(token):
                    state = 'operador'
                elif token in '._':
                    error_sintaxis(inputFile, outputFile)
                elif token != ' ' and token != '\n':
                    error_sintaxis(inputFile, outputFile)

            if token != ' ' and token != '\n':
                unfinishedToken.append(token)


        elif state == 'comentario':
            if token == '\n':
                clearTokensList(unfinishedToken, outputFile)
                if token.isalpha():
                    state = 'variable'
                elif token.isnumeric():
                    state = 'entero'
                elif token == '-':
                    state = 'resta'
                elif token == '/':
                    state = 'division'
                elif isOperand(token):
                    state = 'operador'
                elif token in '._':
                    error_sintaxis(inputFile, outputFile)
            else:
                unfinishedToken.append(token)


        elif state == 'resta':
            if token.isalpha():
                clearTokensList(unfinishedToken, outputFile)
                state = 'variable'
            elif token.isnumeric():
                state = 'entero'
            elif token == '-':
                clearTokensList(unfinishedToken, outputFile)
                state = 'resta'
            elif token == '/':
                clearTokensList(unfinishedToken, outputFile)
                state = 'division'
            elif isOperand(token):
                clearTokensList(unfinishedToken, outputFile)
                state = 'operador'
            elif token == ' ':
                clearTokensList(unfinishedToken, outputFile)
                state = 'inicial'
            elif token in '._':
                error_sintaxis(inputFile, outputFile)
            elif token != ' ' and token != '\n':
                error_sintaxis(inputFile, outputFile)

            if token != ' ' and token != '\n':
                unfinishedToken.append(token)


        elif state == 'real':
            if isInteger(token) or token == 'E' or token == 'e' or token == '-':
                unfinishedToken.append(token)
                state = 'real'
            elif token.isalpha():
                clearTokensList(unfinishedToken, outputFile)
                state = 'variable'
            elif token == '/':
                clearTokensList(unfinishedToken, outputFile)
                state = 'division'
            elif isOperand(token):
                clearTokensList(unfinishedToken, outputFile)
                state = 'token'
            elif token == ' ':
                clearTokensList(unfinishedToken, outputFile)
                state = 'inicial'
            elif token in '._':
                error_sintaxis(inputFile, outputFile)
            elif token != ' ' and token != '\n':
                error_sintaxis(inputFile, outputFile)
            

    # Se termina el loop. Limpiar lo que haya quedado en la lista
    clearTokensList(unfinishedToken, outputFile)



"""Recibe una lista con los caracteres que forman un token y
un archivo. Obtiene los datos del token y los manda a imprimir
en el archivo
"""
def clearTokensList(tokenList, outputFile):

    # Asegurarse de que haya elementos en la lista
    if len(tokenList) < 1:
        return

    tokenData = getToken(tokenList)
    printToken(tokenData[0], tokenData[1], outputFile)

    tokenList.clear()



"""Recibe un token como entrada. Los caracteres del token
están separados en una lista. Regresa una lista con el
token en la primera posicion y su tipo en la segunda posicion
"""
def getToken(tokenList):

    token = ''.join(tokenList).strip()
    tipo = ''

    if isInteger(token):
        tipo = 'Entero'
    elif isVariable(token):
        tipo = 'Variable'
    elif token == '-':
        tipo = 'Resta'
    elif token == '/':
        tipo = 'División'
    elif isFloat(token):
        tipo = 'Real'
    elif isOperand(token):
        tipo = SYMBOLS[token]
    elif isComment(token):
        tipo = 'Comentario'
            
    return [token.strip(), tipo]


"""Recibe el token, su tipo y un archivo. Imprime el token y su tipo
en el archivo recibido y en forma de tabla
"""
def printToken(token, tokenName, f):
    print(token + (' ' * (NUM_ESPACIOS - len(token))) + tokenName, file=f)


"""Recibe un token en forma de string. Regresa un booleano
que indica si el token es un comentario
"""
def isComment(token):
    if len(token) < 2:
        return False
    return token[0:2] == "//"


"""Recibe un token en forma de string. Regresa un booleano
que indica si el token es una variable valida
"""
def isVariable(token):

    if token.isalpha() or token.isalnum() and not isInteger(token[0]):
        return True
    elif '_' in token and token[0] != '_' and not isInteger(token[0]):
        return True

    return False


"""Recibe un token en forma de string. Regresa un booleano
que indica si el token es un entero valido
"""
def isInteger(token):
    try:
        int(token)
        return True
    except ValueError:
        return False


"""Recibe un token en forma de string. Regresa un booleano
que indica si el token es un operador valido
"""
def isOperand(token):
    return token in SYMBOLS


"""Recibe un token en forma de string. Regresa un booleano
que indica si el token es un numero decimal valido
"""
def isFloat(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


"""Si hay un error de sintaxis en el programa, se cierran
archivos y se termina el programa"""
def error_sintaxis(inputFile, outputFile):
    inputFile.close()
    outputFile.close
    print('ERROR DE SINTAXIS. TERMINANDO PROGRAMA', file=outputFile)
    sys.exit()


if __name__ == '__main__':

    # Asegurarse de que el archivo fue dado en la linea de comandos
    if len(sys.argv) != 2:
        print("USO: python -m DFA [ARCHIVO_CON_EXPRESIONES.txt]")
        sys.exit()

    archivo = sys.argv[1]

    # Asegurarse que sea un archivo .txt
    if archivo[-4:] != ".txt":
        print("Debes proveer un archivo .txt")
        sys.exit()

    # Asegurarse de que el archivo exista en el directorio
    if not os.path.isfile(archivo):
        print ("Este archivo no se encuentra en el directorio actual")
        sys.exit()

    lexerAritmetico(archivo)