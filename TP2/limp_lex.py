import ply.lex as lex
# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for:
#   1. numbers
#   2. operations: +,-,*,/
#   3. grouping: ( ) 
#   4. registers: a..z
#   5. read: ?
#   6. print !
# 
# ------------------------------------------------------------
import ply.lex as lex
import sys

# List of token names.   This is always required
reserved = {
    'int' : 'INT',
    'print' : 'PRINT',
    'read' : 'READ',
    'dump' : 'DUMP',
    'if'   : 'IF',
    'else' : 'ELSE',
}

tokens = [
    'number', 'id', 'BEGIN', 'MI', 'ME', 
 ] + list(reserved.values())

# Literals
literals = ['+', '-', '*', '/', '(', ')', '{', '}', '?', '!', ';', '=', '[', ']', '&', '|', '!', '>', '<']
t_BEGIN = r'BEGIN'
t_MI = r'>='
t_ME = r'<='
# A regular expression rule with some action code

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



 
#----------------------------------------
# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    print('new line')
    t.lexer.lineno += len(t.value)
    t.lexer.skip(1)
 
# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
 
# Error handling rule
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
 
