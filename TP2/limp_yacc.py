# Ricardo Leal A75411
# Renato Cruzinha A75310

import sys
import ply.yacc as yacc
from limp_lex import tokens


def p_Limp(p): 
    "Limp : BlocoDeclaracoes BEGIN BlocoInstrucoes"
    print(p[1], 'START', p[3], 'STOP')

def p_BlocoDeclaracoes(p):
    "BlocoDeclaracoes : Declaracao"
    p[0] = p[1]

def p_BlocoDeclaracoes_list(p):
    "BlocoDeclaracoes : BlocoDeclaracoes Declaracao"
    p[0] = p[1] + ' ' + p[2]

def p_BlocoInstrucoes(p):
    "BlocoInstrucoes : Instrucao"
    p[0] = p[1]

def p_BlocoInstrucoes_list(p):
    "BlocoInstrucoes : BlocoInstrucoes Instrucao"
    p[0] = p[1] + ' ' + p[2]

def p_Declaracao_var(p):
    "Declaracao : DeclVar ';'"
    p[0] = p[1]

def p_Declaracao_array(p):
    "Declaracao : DeclArray ';'"
    p[0] = p[1]

def p_Declaracao_array_bi(p):
    "Declaracao : DeclArrayBi ';'"
    p[0] = p[1]

def p_Declaracao_fun(p):
    "Declaracao : DeclFun"
    p[0]=p[1]

def p_DeclVar_atrib(p):
    "DeclVar : INT id '=' ExpA"
    if p[2] in p.parser.registers:
        print('Erro: Variável já em uso')
        pass
    else:
        registo = {}
        registo['tipo'] = p[1]
        registo['gp'] = p.parser.gp
        p.parser.registers.update({p[2] : registo})
        p.parser.gp+=1

        p[0] = p[4]
    
def p_DeclVar(p):
    "DeclVar : INT id"
    if p[2] in p.parser.registers:
        print('Erro: Variável já em uso')
        pass
    else:
        registo = {}
        registo['tipo'] = p[1]
        registo['gp'] = p.parser.gp
        p.parser.registers.update({p[2] : registo})
        p.parser.gp+=1

        p[0] = ' PUSHI 0 '

def p_DeclArray(p):
    "DeclArray : INT id '[' number ']'"
    if p[2] in p.parser.registers:
        print('Erro: Variável já em uso')
        pass
    else:
        registo = {}
        registo['tipo'] = 'array'
        registo['gp'] = p.parser.gp
        registo['tamanho'] = p[4] + 1
        p.parser.registers.update({p[2] : registo})
        p.parser.gp+=int(p[4])+1

        p[0] = ' PUSHN ' + str(p[4]+1)

def p_DeclArrayBi(p):
    "DeclArrayBi : INT id '[' number ']' '[' number ']'"
    if p[2] in p.parser.registers:
        print('Erro: Variável já em uso')
        pass
    else:
        registo = {}
        tamanho=int((p[4]+1) * (p[7]+1))
        registo['tipo'] = 'array-bi'
        registo['gp'] = p.parser.gp
        registo['tamanho'] = tamanho
        p.parser.registers.update({p[2] : registo})
        p.parser.gp+=tamanho

        p[0] = ' PUSHN ' + str(tamanho)

def p_DeclFun(p):
    "DeclFun : FUNCTION  id '(' ')' '{' BlocoInstrucoes RETURN ExpRel ';' '}'"
    if p[2] in p.parser.registers:
        print('Erro: Funcao já em uso')
        pass
    else:
        registo = {}
        registo['tipo'] = 'fun'
        registo['gp'] = p.parser.gp + 1
        registo['gp-var'] = p.parser.gp
        p.parser.registers.update({p[2] : registo})
        p.parser.gp+=1
        label_fun=p[2] + ':'
        function_end=p[2] + 'end '
    p[0] = ' PUSHI 0 JUMP '+ function_end + label_fun + p[6] + p[8] + ' STOREG ' + str(p.parser.registers.get(p[2])['gp-var']) + ' RETURN ' + function_end + ':'

def p_Instrucao_dump(p):
    "Instrucao : DUMP"
    print("Registers: ", p.parser.registers)

def p_Instrucao_print(p):
    "Instrucao : PRINT ExpA ';'"
    p[0] = p[2] + ' WRITEI '

def p_Instrucao_printa(p):
    "Instrucao : PRINTA id ';'"
    if p[2] in p.parser.registers:
        print('entrou')
        label_array_begin = ' ' + p[2] + 'begin'
        label_array_end = ' ' + p[2] + 'end'
        tamanho = str(p.parser.registers.get(p[2])['tamanho'])
        pos_i = str(p.parser.varsControlo.get('varprinta'))
        p.parser.gp+=1
    else:
        print('Erro: Array não declarado/Argumento tem de ser um array')
        pass
    p[0] = ' PUSHI 0 STOREG ' + pos_i + label_array_begin + ': ' + ' PUSHG ' + pos_i + ' PUSHI ' + tamanho + ' INF JZ ' + label_array_end + ' PUSHGP PUSHI ' + str(p.parser.registers.get(p[2])['gp']) + ' PADD PUSHG ' + pos_i + ' LOADN WRITEI PUSHG ' + pos_i + ' PUSHI 1 ADD STOREG ' + pos_i + ' JUMP ' + label_array_begin + ' ' + label_array_end + ':'

def p_Instrucao_read_var(p):
    "Instrucao : READ id ';'"
    p[0] = 'READ ATOI STOREG ' + str(p.parser.registers.get(p[2])['gp'])

def p_Instrucao_read_array(p):
    "Instrucao : READ id '[' number ']' ';'"
    p[0] = 'PUSHGP PUSHI ' + str(p.parser.registers.get(p[2])['gp']) + ' PADD READ ATOI STOREN'

def p_Instrucao_atrib(p):
    "Instrucao : Atribuicao ';'"
    p[0] = p[1]

def p_Atribuicao_var(p):
    "Atribuicao : AtrVar"
    p[0]=p[1]

def p_Atribuicao_array(p):
    "Atribuicao : AtrArray"
    p[0]=p[1]

def p_Atribuicao_array_bi(p):
    "Atribuicao : AtrArrayBi"
    p[0]=p[1]

def p_Atribuicao_fun(p):
    "Atribuicao : AtrFun"
    p[0]=p[1]

def p_AtrVar(p):
    "AtrVar : id '=' ExpA"
    p[0] = p[3] + ' STOREG ' + str(p.parser.registers.get(p[1])['gp'])

def p_AtrArray(p):
    "AtrArray : id '[' number ']' '=' ExpA"
    p[0] = ' PUSHGP PUSHI ' + str(p.parser.registers.get(p[1])['gp']) + ' PADD PUSHI ' + str(p[3]) + p[6] + ' STOREN ' 

def p_AtrArrayBi(p):
    "AtrArrayBi : id '[' number ']' '[' number ']' '=' ExpA"
    p[0] = ' PUSHGP PUSHI ' + str(p.parser.registers.get(p[1])['gp']) + ' PADD PUSHI ' + str((p[3]+1) * (p[6]+1)) + p[9] + ' STOREN ' 

def p_AtrFun(p):
    "AtrFun : id '='  id '(' ')'"
    p[0] = ' PUSHA ' + p[3] + ' CALL PUSHG ' + str(p.parser.registers.get(p[3])['gp-var']) + ' STOREG '+str(p.parser.registers.get(p[1])['gp'])

def p_Instrucao_condicionais(p):
    "Instrucao : Condicional"
    p[0]=p[1]

def p_Condicional_if(p):
    "Condicional : IF '(' Condicao ')' '{' BlocoInstrucoes '}'"
    label='fimif'+str(p.parser.contaIfs)
    p.parser.contaIfs += 1
    p[0] = p[3] + ' JZ ' + label + p[6] + label + ':'

def p_Condicional_if_else(p):
    "Condicional : IF '(' Condicao ')' '{' BlocoInstrucoes '}' ELSE '{' BlocoInstrucoes '}'"
    label_else='else'+str(p.parser.contaIfs)
    label_fim='fimif'+str(p.parser.contaIfs)
    p.parser.contaIfs += 1
    p[0]= p[3] + ' JZ ' + label_else + p[6] + ' JUMP ' + label_fim + ' ' + label_else + ':' + p[10] + label_fim + ':'

def p_Condicional_repeat_until(p):
    "Condicional : REPEAT '{' BlocoInstrucoes '}' UNTIL '(' Condicao ')'"
    label_ciclo = 'ciclo'+ str(p.parser.contaCiclos)
    p.parser.contaCiclos += 1
    p[0] = label_ciclo + ':' + p[3]  + p[7] + ' JZ ' + label_ciclo

def p_Condicional_while_do(p):
    "Condicional : WHILE '(' Condicao ')' DO '{' BlocoInstrucoes '}'"
    label_inicio_ciclo = ' iniciociclo'+ str(p.parser.contaCiclos)
    label_fim_ciclo = ' fimciclo'+ str(p.parser.contaCiclos)
    p.parser.contaCiclos += 1
    p[0] = label_inicio_ciclo + ':' + p[3] + ' JZ ' + label_fim_ciclo + p[7] + ' JUMP ' + label_inicio_ciclo + label_fim_ciclo + ':'

def p_Condicao(p):
    "Condicao : ExpLogOr"
    p[0]=p[1]

def p_ExpLogOr(p):
    "ExpLogOr : ExpLogAnd"
    p[0]=p[1]

def p_ExpLogOr_or(p):
    "ExpLogOr : ExpLogOr OR ExpLogAnd"
    p[0] = p[1] + p[3] + ' ADD ' + p[1] + p[3] + ' MUL SUB '

def p_ExpLogAnd(p):
    "ExpLogAnd : ExpLogNot"
    p[0]=p[1]

def p_ExpLogAnd_and(p):
    "ExpLogAnd : ExpLogAnd AND ExpLogOr"
    p[0] = p[1] + p[3] + ' MUL '

def p_ExpLogNot(p):
    "ExpLogNot : ExpEq"
    p[0] = p[1]

def p_ExpLogNot_not(p):
    "ExpLogNot : NOT Condicao"
    p[0] = p[2] + ' NOT '

def p_ExpEq(p):
    "ExpEq : ExpRel"
    p[0] = p[1]

def p_ExpEq_eq(p):
    "ExpEq : ExpEq EQ ExpRel"
    p[0] = p[1] + p[3] + ' EQUAL '

def p_ExpEq_ne(p):
    "ExpEq : ExpEq NE ExpRel"
    p[0] = p[1] + p[3] + ' EQUAL NOT '

def p_ExpRel(p):
    "ExpRel : ExpA"
    p[0] = p[1]

def p_ExpRel_g(p):
    "ExpRel : ExpRel '>' ExpA"
    p[0] = p[1] + p[3] + ' SUP '

def p_ExpRel_l(p):
    "ExpRel : ExpRel '<' ExpA"
    p[0] = p[1] + p[3] + ' INF '

def p_ExpRel_ge(p):
    "ExpRel : ExpRel GE ExpA"
    p[0] = p[1] + p[3] + ' SUPEQ '

def p_ExpRel_le(p):
    "ExpRel : ExpRel LE ExpA"
    p[0] = p[1] + p[3] + ' INFEQ '

def p_Exp_add(p):
    "ExpA : ExpA '+' Term"
    p[0] = p[1] + p[3] + ' ADD '

def p_Exp_sub(p):
    "ExpA : ExpA '-' Term"
    p[0] = p[1] + p[3] + ' SUB '

def p_Exp_term(p):
    "ExpA : Term"
    p[0] = p[1]

def p_Term_mul(p):
    "Term : Term '*' Factor"
    p[0] = p[1] + p[3] + ' MUL '

def p_Term_div(p):
    "Term : Term '/' Factor"
    p[0] = p[1] + p[3] + ' DIV '

def p_Term_factor(p):
    "Term : Factor"
    p[0] = p[1]

def p_Factor_id(p):
    "Factor : id"
    p[0] = ' PUSHG ' + str(p.parser.registers.get(p[1])['gp'])

def p_Factor_number(p):
    "Factor : number"
    p[0] = ' PUSHI ' + str(p[1])

def p_Factor_group(p):
    "Factor : '(' ExpA ')'"
    p[0] = p[2]

def p_Factor_array(p):
    "Factor : id '[' number ']'"
    p[0] = ' PUSHGP PUSHI ' + str(p.parser.registers.get(p[1])['gp']) + ' PADD PUSHI ' + str(p[3]) + ' LOADN ' 

def p_Factor_array_bi(p):
    "Factor : id '[' number ']' '[' number ']'"
    p[0] = ' PUSHGP PUSHI ' + str(p.parser.registers.get(p[1])['gp']) + ' PADD PUSHI ' + str((p[3]+1) * (p[6]+1)) + ' LOADN ' 

def p_Factor_true(p):
    "Factor : TRUE"
    p[0] = ' PUSHI 1 '

def p_Factor_false(p):
    "Factor : FALSE"
    p[0] = ' PUSHI 0 '

#----------------------------------------
def p_error(p):
    print('Syntax error: ', p)
    parser.success = False

#----------------------------------------
#inicio do Parser
parser = yacc.yacc()

parser.success = True
parser.registers = {}   #tabela de identificadores
parser.gp = 0           # offset em relacao ao global pointer(gp)
parser.contaIfs = 0
parser.contaCiclos = 0
parser.varsControlo = {'varprinta' : parser.gp}
parser.gp+=1
print('PUSHI 0')
for line in sys.stdin:
    parser.parse(line)
