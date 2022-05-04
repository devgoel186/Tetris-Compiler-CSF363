'''
NOTE: PLEASE DOWNLOAD PLY, THE PYTHON LEX-YACC FROM HERE: https://www.dabeaz.com/ply/ 
IT IS NOT AVAILABLE FOR DOWNLOAD THROUGH PIP/CONDA

'''

# In this tetris_lexer.py, we do not try to parse Arrays/Matrices, instead we directly return a stream of induvidual tokens

import ply.lex as lex
import ply.yacc as yacc
import sys
from Level import Level


# Defining the Reserved Keywords.
reserved = {
    'level': 'LEVEL',
    'setlevelspeed': 'SETLEVELSPEED',
    'passlevellines': 'PASSLEVELLINES',
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
    'RIGHT_SQR',
    'LEFT_SQR',
    'SEMICOLON',
    'COMMA',
    'MULTIPLY',
    'ARROWSIGN',
    
    # Comments and blank/whitespace:
    'COMMENT',
    'BLANKS',
    
] + list(reserved.values())

t_EQUALS = r'='
t_LEFT_BRT = r'\('
t_RIGHT_BRT = r'\)'
t_LEFT_CURLY = r'\{'
t_RIGHT_SQR = r'\['
t_LEFT_SQR = r'\]'
t_RIGHT_CURLY = r'\}'
t_SEMICOLON = r'\;'
t_COMMA = r'\,'
t_MULTIPLY = r'\*'

t_ARROWSIGN = r'\>'

t_ignore = r' ' # Ignore Whitespaces

# More complicated tokens, such as tokens that are more than 1 character in length are defined using functions.

# Although blankspace is detected by t_ignore, we have to also detect tokens like \t, \n, \r
def t_BLANKS(t):
    r'[ \t\r\n]+'
    t.lexer.skip(0)

def t_COMMENT(t):
    r'\/\*.*\*\/'
    t.lexer.skip(0)

def t_RES(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')    # Check for reserved words
    return t

def t_INT(t):
    r'[+-]?[0-9]+'
    t.value = int(t.value)
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
    
lexer = lex.lex()




'''
---------    PARSER  ----------------
'''


cur_level = None
cur_level_name = None
levelmap = {}


def p_level(p):
    '''
    level           : LEVEL IDENTIFIER ARROWSIGN
                    | moveconfig SEMICOLON
                    | setlevelspeed SEMICOLON
                    | passlevellines SEMICOLON
                    | board_assign SEMICOLON
                    | piece_definition SEMICOLON
                    | speed SEMICOLON
                    | piececolor SEMICOLON
                    | sequence_definition SEMICOLON
                    | scoring SEMICOLON
                    | random SEMICOLON
                    | startgame SEMICOLON
                    | empty
    '''
    global cur_level, cur_level_name, levelmap
    if(len(p) == 4 and p[3] == '>'):
        if(cur_level_name != p[2]):
            cur_level_name = p[2]
            cur_level = Level(cur_level_name)
            levelmap[cur_level_name] = cur_level
            print(levelmap[cur_level_name])
            
    print(p[1])

# def p_many_levels(p):
#     '''
#     many_levels : many_levels level
#                 | level
#     '''
#     p[0] = p[1]

    
# def p_tetris_compiler(p):
    
#     '''
#     tetris_compiler : tetris_compiler tetris_compiler
#                     | LEVEL IDENTIFIER LEFT_CURLY many_levels RIGHT_CURLY
                    
#     '''
#     if(p[1] != cur_level):
#         cur_level_name = p[1]
#         cur_level = Level(cur_level_name)
#         levelmap[cur_level_name] = cur_level
#         print("Adding new level class!")
        
#     p[0] = p[1]
#     print(p[1])

def p_setlevelspeed(p):
    '''
    setlevelspeed : SETLEVELSPEED LEFT_BRT INT RIGHT_BRT 
    '''
    levelmap[cur_level_name].levelspeed = p[3]
    p[0] = (p[1], p[3])
    
def p_passlevellines(p):
    '''
    passlevellines : PASSLEVELLINES LEFT_BRT INT RIGHT_BRT 
    '''
    levelmap[cur_level_name].pass_lines = p[3]
    p[0] = (p[1], p[3])
    
def p_moveconfig(p):
    '''
    moveconfig : MOVECONFIG LEFT_BRT WASD RIGHT_BRT 
               | MOVECONFIG LEFT_BRT ARROW RIGHT_BRT
    '''
    print(p[3])
    levelmap[cur_level_name].moveconfig = p[3]
    p[0] = (p[1], p[3])

def p_board_assign(p):
    '''
    board_assign : BOARD EQUALS INT COMMA INT
    '''
    levelmap[cur_level_name].board = (p[3], p[5])
    p[0] = (p[1], p[3], p[5])
    
def p_piece_definition(p):
    '''
    piece_definition : PIECE IDENTIFIER EQUALS matrix
    '''
    # class attribute pieces is hence an array of tuples (a, b) where a is the identifier, b is the matrix representing piece
    levelmap[cur_level_name].pieces_list[p[2]] = p[4]
    p[0] = (p[1], p[2], p[4])
    

def p_array(p):
    '''
    array : RIGHT_SQR group_of_types LEFT_SQR
    '''
    p[0] = p[2]
    
def p_matrix(p):
    '''
    matrix : RIGHT_SQR group_of_arrays LEFT_SQR 
    '''
    p[0] = p[2]

def p_type(p):
    '''
    type : INT 
         | IDENTIFIER
    '''
    p[0] = p[1]
    
def p_expression(p):
    '''
    expression : IDENTIFIER
               | IDENTIFIER MULTIPLY INT
    '''
    if(len(p) < 3):
        p[0] = (p[1], 1)
    else:
        p[0] = (p[1], p[3])

def p_group_of_expressions(p):
    '''
    group_of_expressions : group_of_expressions COMMA expression
                         | expression
    '''
    if(len(p) > 2):
        p[1].append(p[3])
    
    else:
        intval = p[1]
        p[1] = []
        p[1].append(intval)
        
    p[0] = p[1]
        
def p_group_of_types(p):
    '''
    group_of_types : group_of_types COMMA type
                   | type
    '''
    if(len(p) > 2):
        p[1].append(p[3])
    
    else:
        intval = p[1]
        p[1] = []
        p[1].append(intval)
        
    p[0] = p[1]
    
def p_group_of_arrays(p):
    '''
    group_of_arrays : group_of_arrays COMMA array
                    | array
    '''
    if(len(p) > 2):
        p[1].append(p[3])
    
    else:
        arrayval = p[1]
        p[1] = []
        p[1].append(arrayval)
        
    p[0] = p[1]
    
    
def p_speed(p):
    '''
    speed : SPEED LEFT_BRT IDENTIFIER COMMA INT RIGHT_BRT
    '''
    levelmap[cur_level_name].piece_speeds[p[3]] =  p[5]
    p[0] = (p[1], p[3], p[5])
    
def p_piececolor(p):
    '''
    piececolor : PIECECOLOR LEFT_BRT IDENTIFIER COMMA COLORNAME RIGHT_BRT
               | PIECECOLOR LEFT_BRT IDENTIFIER COMMA HEXCOLOR RIGHT_BRT
    '''
    levelmap[cur_level_name].colors_list[p[3]] = p[5]
    p[0] = (p[1], p[3], p[5])

def p_sequence_definition(p):
    '''
    sequence_definition : SEQUENCE IDENTIFIER EQUALS array
    '''
    levelmap[cur_level_name].sequences_list[p[2]] = p[4]
    p[0] = (p[1], p[2], p[4])
    
def p_scoring(p):
    '''
    scoring : SCORING EQUALS array
    '''
    levelmap[cur_level_name].scoring = p[3]
    p[0] = (p[1], p[3])

def p_random(p):
    '''
    random : RANDOM LEFT_BRT IDENTIFIER RIGHT_BRT
           | RANDOM LEFT_BRT empty RIGHT_BRT
    '''
    if(p[3] == None):
        levelmap[cur_level_name].random_settings["global"] = True
    else:
        levelmap[cur_level_name].random_settings[p[3]] = True
        
    p[0] = (p[1], p[3])
    
    
def p_startgame(p):
    '''
    startgame : STARTGAME LEFT_BRT group_of_expressions RIGHT_BRT
    '''
    levelmap[cur_level_name].startgame_list = p[3]
    p[0] = (p[1], p[3])
    
def p_empty(p):
    '''
    empty :
    '''
    p[0] = None
    
def p_error(p):
    print(f"Syntax error in input! Exiting!")
    exit()
    
    
parser = yacc.yacc(start='level')
    
filename = 'game_final.ttr'
with open(filename, 'r') as file:
    for line in file:
        parser.parse(line)

print('\n\nFINAL GAME FEED\n-------------------------------------------')


for key in levelmap:
#     from pprint import pprint
#     print(key)
#     pprint(vars(levelmap[key]))
    
    from game_config import set_parameters
    set_parameters(levelmap)