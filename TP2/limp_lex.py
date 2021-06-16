# Ricardo Leal A75411
# Renato Cruzinha A75310

import ply.lex as lex
import sys

# reserved
reserved = {
    'int' : 'INT',
    'print' : 'PRINT',
    'printa' : 'PRINTA',
    'read' : 'READ',
    'dump' : 'DUMP',
    'if'   : 'IF',
    'else' : 'ELSE',
    'repeat' : 'REPEAT',
    'until'  :  'UNTIL',
    'function' : 'FUNCTION',
    'return'   : 'RETURN',
    'while'    : 'WHILE',
    'do'       : 'DO',
}

# tokens
tokens = [
    'number', 'id', 'BEGIN', 'EQ', 'NE', 'GE', 'LE', 'AND', 'NOT', 'OR', 'TRUE', 'FALSE',
 ] + list(reserved.values())

# literals
literals = ['+', '-', '*', '/', '(', ')', '{', '}', '?', ';', '=', '[', ']', '>', '<', '%']
t_BEGIN = r'BEGIN'

# regular expression
def t_EQ(t):
    r'=='
    return t

def t_NE(t):
    r'!='
    return t

def t_GE(t):
    r'>='
    return t

def t_LE(t):
    r'<='
    return t

def t_AND(t):
    r'&&'
    return t

def t_OR(t):
    r'\|\|'
    return t

def t_NOT(t):
    r'!'
    return t

def t_id(t):
    r'[a-z]+'
    t.type = reserved.get(t.value,'id')
    return t

def t_VARS(t):
    r'VARS'
    return t

def t_number(t):
    r'\d+'
    t.value = int(t.value)    
    t.lexer.num_count += 1
    return t

def t_TRUE(t):
    r'True'
    return t

def t_FALSE(t):
    r'False'
    return t
#----------------------------------------

# track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexer.skip(1)
 
# string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
 
# error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

 # EOF handling rule
#def t_eof(t):
  # Get more input (Example)
  #more = input('... ')
  #if more:
  #    self.lexer.input(more)
  #    return self.lexer.token()
  #return None

#----------------------------------------
# Build the lexer
lexer = lex.lex()
lexer.num_count = 0


 
