operadores = {"=":"Asignacion", "+":"Suma", "-":"Resta", "*":"Multiplicacion", "/":"Division", "^":"Potencia"}

def IsComment(token):
    if len(token) < 2   : return False
    return token[0:2] == "//"

def IsVariable(token):
    if not token[0].isalpha() : return False
    
    for i in range(1,len(token)):
        if not (token[i].isalpha() or token[i].isnumeric() or token[i] == "_"):
            return False
        
    return True

def isNumber(token):
    try:
        float(token)
        return True
    except ValueError:
        return False

def isOperand(token):
    return token in operadores


'''
@ nombre_archivo es el nombre del archivo a leer.
Entrada:
- Un archivo tipo texto que contenga una o más expresiones aritméticas, una por renglón.
- Los tokens no necesariamente deben estar separados por un blanco, o pueden tener separación de más de un blanco
'''
def lexerAritmetico(nombre_archivo):
    f = open(nombre_archivo)
    
    for line in f.readlines():
        print(line)
        
lexerAritmetico("expresiones.txt")
            

