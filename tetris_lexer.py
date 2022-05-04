'''
NOTE: PLEASE DOWNLOAD PLY, THE PYTHON LEX-YACC FROM HERE: https://www.dabeaz.com/ply/ 
IT IS NOT AVAILABLE FOR DOWNLOAD THROUGH PIP/CONDA

'''

import ply.lex as lex
import sys

# Defining the Reserved Keywords.
reserved = {
    'level': 'LEVEL',
    'setlevelspeed': 'SETLEVELSPEED',
    'passlevelscore': 'PASSLEVELSCORE',
    'board': 'BOARD',
    
    'piece': 'PIECE',
    'speed': 'SPEED',
    'piececolor': 'PIECECOLOR',
    'bonus': 'BONUS',
    
    'sequence': 'SEQUENCE',
    'random': 'RANDOM',
    'startgame':'STARTGAME',
    'scoring': 'SCORING',
    'skipblock': 'SKIPBLOCK',
    'moveconfig': 'MOVECONFIG',
    'simultaneous': 'SIMULATANEOUS',
    'WASD': 'WASD', # WASD Movement Key Config
    'ARROW': 'ARROW', # Arrow Keys Movement Key Config
}

tokens = [  
    'RES', # Reserved Gamewords
    'IDENTIFIER', # Variables for Pieces and sequences
    
    # Types
    'INT',
    'COLORNAME', # Color names for pieces
    'HEXCOLOR',
    'MATRIX', # A matrix is used to specify a piece structure 
    'ARRAY', # An array is used to specify sequences of pieces, and also the points scheme
    
    # Punctuations/Operators
    'EQUALS',
    'LEFT_BRT',
    'RIGHT_BRT',
    'LEFT_CURLY',
    'RIGHT_CURLY',
    'SEMICOLON',
    'COMMA',
    'MULTIPLY',
    
    # Comments and blank/whitespace:
    'COMMENT',
    'BLANKS',
    
] + list(reserved.values())

t_EQUALS = r'='
t_LEFT_BRT = r'\('
t_RIGHT_BRT = r'\)'
t_LEFT_CURLY = r'\{'
t_RIGHT_CURLY = r'\}'
t_SEMICOLON = r'\;'
t_COMMA = r'\,'
t_MULTIPLY = r'\*'

t_ignore = r' ' # Ignore Whitespaces

# More complicated tokens, such as tokens that are more than 1 character in length are defined using functions.

# Although blankspace is detected by t_ignore, we have to also detect tokens like \t, \n, \r
def t_BLANKS(t):
    r'[\t\r\n]+'
    t.type = 'BLANKS'
    t.lexer.skip(0)

def t_COMMENT(t):
    r'\/\*.*\*\/'
    t.type = 'COMMENT'
    return t

def t_RES(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')    # Check for reserved words
    return t

def t_INT(t):
    r'[+-]?[0-9]+'
    t.value = int(t.value)
    return t

# The following Pattern is tentative, as mentioned in the report
def t_MATRIX(t):
    r'\[\[[^\;]*\]\]'    
    try:
        c = str(t.value)[1:-1].split(']')
        d = []
        for i in range(len(c) - 1):
            d.append(c[i].split('[')[1])
            
        e = []
        for item in d:
            e.append(item.split(','))

        ret_val = []
        for item in e:
            cur = []
            for number in item:
                k = int(number)
                cur.append(k)
            ret_val.append(cur)
        
        t.value = ret_val
        return t
    
    except:
        print("COMPILE ERROR")
        return "COMPILE_ERROR"
        
        
# The following Pattern is tentative, as mentioned in the report
def t_ARRAY(t):
    r'\[[^\;\[]*\]'
    items = str(t.value)[1:-1].split(',')
    for item in items:
        try:
            item = int(item)
        except:
            item = item.strip()
          
    t.value = items
    return t

def t_COLORNAME(t):
    r"\'[a-z]+\'"
    t.type = 'COLORNAME'
    return t

def t_HEXCOLOR(t):
    r'\#[A-Fa-f0-9]{6}|[A-Fa-f0-9]{3}'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_error(t):
    print("Compilation Error! - ")
    return t
    


if(__name__ == "__main__"):
    # Build the lexer
    lexer = lex.lex()
    filename = str(input())
    inp = None
    with open(filename, 'r') as file:
        inp = file.read()
    lexer.input(inp)

    
    fail = 0
    while True:
        tok = lexer.token()
        if not tok:
            break
        
        if(tok == 'COMPILE_ERROR'):
            print("Compilation Error\n")
            fail = 1
            break
        print(tok)
        
    if(fail == 0):
        print("Compiled Succesfully!\n")