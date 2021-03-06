# ------------------------------------------------------------
# 
#   
# ------------------------------------------------------------

import sys
import ply.yacc as yacc
from limp_lex import tokens


def p_Limp(p): 
    "Limp : BlocoDeclaracoes BEGIN BlocoInstrucoes"
    print('1')
    print( p[1], 'START', p[3], 'STOP')
    pass

def p_BlocoDeclaracoes(p):
    "BlocoDeclaracoes : Declaracao"
    print('2-1')
    p[0] = p[1]

def p_BlocoDeclaracoes_list(p):
    "BlocoDeclaracoes : BlocoDeclaracoes Declaracao"
    print('3')
    p[0] = p[1] + ' ' + p[2]

def p_BlocoInstrucoes(p):
    "BlocoInstrucoes : Instrucao"
    print('4')
    p[0] = p[1]

def p_BlocoInstrucoes_list(p):
    "BlocoInstrucoes : BlocoInstrucoes Instrucao"
    print('5')
    p[0] = p[1] + ' ' + p[2]

def p_Declaracao_var(p):
    "Declaracao : DeclVar ';'"
    print('6')
    p[0] = p[1]

def p_Declaracao_array(p):
    "Declaracao : DeclArray ';'"
    print('6-1')
    p[0] = p[1]

def p_Declaracao_fun(p):
    "Declaracao : DeclFun"
    print('6-2')
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

        #p[0] = p[4] + ' STOREG ' + str(p.parser.registers.get(p[2]))
        p[0] = p[4]
    print('7 - Nova variável tipo: ', p[1], 'nome: ',  p[2], 'ExpA/Valor: ', p[4])
    
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
    print('8 - Nova variável tipo: ', p[1], 'nome: ',  p[2] )

def p_DeclArray(p):
    "DeclArray : INT id '[' number ']'"
    if p[2] in p.parser.registers:
        print('Erro: Variável já em uso')
        pass
    else:
        registo = {}
        registo['tipo'] = 'array'
        registo['gp'] = p.parser.gp
        registo['tamanho'] = p[4]
        p.parser.registers.update({p[2] : registo})
        p.parser.gp+=int(p[4])

        p[0] = ' PUSHN ' + str(p[4])
    print('8 - Nova variável tipo: ', p[1], 'nome: ',  p[2] )

def p_DeclFun(p):
    "DeclFun : FUNCTION  id '(' ')' '{' BlocoInstrucoes RETURN ExpRel '}'"
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
    p[0] = 'PUSHI 0 ' + label_fun + p[6] + p[8] + ' STOREG ' + str(p.parser.registers.get(p[2])['gp-var'])

def p_Instrucao_dump(p):
    "Instrucao : DUMP"
    print('9')
    print("Registers: ", p.parser.registers)

def p_Instrucao_print(p):
    "Instrucao : PRINT ExpA ';'"
    print('10')
    p[0] = p[2] + ' WRITEI '
    #print(p.parser.registers.get(p[2]))

def p_Instrucao_read_var(p):
    "Instrucao : READ id ';'"
    print('11')
    p[0] = 'READ ATOI STOREG ' + str(p.parser.registers.get(p[2])['gp'])
    #valor = input("Introduza um valor inteiro: ")
    #p.parser.registers.update({p[2] : int(valor)})
    #print(f"Adicionado registo: {p[2]} = {valor}")

def p_Instrucao_read_array(p):
    "Instrucao : READ id '[' number ']' ';'"
    print('11-1')
    p[0] = 'PUSHGP PUSHI ' + str(p.parser.registers.get(p[2])['gp']) + ' PADD READ ATOI STOREN'
    #valor = input("Introduza um valor inteiro: ")
    #p.parser.registers.update({p[2] : int(valor)})
    #print(f"Adicionado registo: {p[2]} = {valor}")

def p_Instrucao_atrib(p):
    "Instrucao : Atribuicao ';'"
    print('11-1')
    p[0] = p[1]

def p_Atribuicao_var(p):
    "Atribuicao : AtrVar"
    p[0]=p[1]

def p_Atribuicao_array(p):
    "Atribuicao : AtrArray"
    p[0]=p[1]

def p_Atribuicao_fun(p):
    "Atribuicao : AtrFun"
    p[0]=p[1]

def p_AtrVar(p):
    "AtrVar : id '=' ExpA"
    print('11-1')
    p[0] = p[3] + ' STOREG ' + str(p.parser.registers.get(p[1])['gp'])

def p_AtrArray(p):
    "AtrArray : id '[' number ']' '=' ExpA"
    print('11-2')
    p[0] = ' PUSHGP PUSHI ' + str(p.parser.registers.get(p[1])['gp']) + ' PADD PUSHI ' + str(p[3]) + p[6] + ' STOREN ' 

def p_AtrFun(p):
    "AtrFun : id '='  id '(' ')'"
    print('AtrFun')
    p[0] =' PUSHG ' + str(p.parser.registers.get(p[3])['gp-var']) + ' STOREG '+str(p.parser.registers.get(p[1])['gp'])
   #p[0]= ' PUSHA ' + p[3] + ' CALL STOREG ' + str(p.parser.registers.get(p[1])['gp-var'])

def p_Instrucao_condicionais(p):
    "Instrucao : Condicional"
    print('condicional')
    p[0]=p[1]

def p_Condicional_if(p):
    "Condicional : IF '(' Condicao ')' '{' BlocoInstrucoes '}'"
    print('condicional if')
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
    print("Condicional : REPEAT '{' BlocoInstrucoes '}' 'UNTIL' '(' Condicao ')'")
    label_ciclo = 'ciclo'+ str(p.parser.contaCiclos)
    p.parser.contaCiclos += 1
    p[0] = label_ciclo + ':' + p[3]  + p[7] + ' JZ ' + label_ciclo

def p_Condicao(p):
    "Condicao : ExpLogOr"
    print('Condicao : ExpLogOr')
    p[0]=p[1]

def p_ExpLogOr(p):
    "ExpLogOr : ExpLogAnd"
    print('ExpLogOr : ExpLogAnd')
    p[0]=p[1]

def p_ExpLogOr_or(p):
    "ExpLogOr : ExpLogOr OR ExpLogAnd"
    print('ExpLogOr : ExpLogOr OR ExpLogAnd')
    p[0] = p[1] + p[3] + ' ADD ' + p[1] + p[3] + ' MUL SUB '

def p_ExpLogAnd(p):
    "ExpLogAnd : ExpLogNot"
    print('ExpLogAnd : ExpLogNot')
    p[0]=p[1]

def p_ExpLogAnd_and(p):
    "ExpLogAnd : ExpLogAnd AND ExpLogOr"
    print('ExpLogAnd : ExpLogAnd AND ExpLogOr')
    p[0] = p[1] + p[3] + ' MUL '

def p_ExpLogNot(p):
    "ExpLogNot : ExpEq"
    print('ExpLog : ExpEq')
    p[0] = p[1]

def p_ExpLogNot_not(p):
    "ExpLogNot : NOT Condicao"
    print('ExpLog : NOT Condicao')
    p[0] = p[2] + ' NOT '

def p_ExpEq(p):
    "ExpEq : ExpRel"
    print('ExpEq : ExpRel')
    p[0] = p[1]

def p_ExpEq_eq(p):
    "ExpEq : ExpEq EQ ExpRel"
    print('ExpEq : ExpEq EQ ExpRel')
    p[0] = p[1] + p[3] + ' EQUAL '

def p_ExpEq_ne(p):
    "ExpEq : ExpEq NE ExpRel"
    print('ExpEq : ExpEq NE ExpRel')
    p[0] = p[1] + p[3] + ' EQUAL NOT '

def p_ExpRel(p):
    "ExpRel : ExpA"
    print('ExpRel')
    p[0] = p[1]

def p_ExpRel_g(p):
    "ExpRel : ExpRel '>' ExpA"
    print('ExpRel : ExpRel > ExpA')
    p[0] = p[1] + p[3] + ' SUP '

def p_ExpRel_l(p):
    "ExpRel : ExpRel '<' ExpA"
    print('ExpRel : ExpRel > ExpA')
    p[0] = p[1] + p[3] + ' INF '

def p_ExpRel_ge(p):
    "ExpRel : ExpRel GE ExpA"
    print('ExpRel : ExpRel GE/>= ExpA')
    p[0] = p[1] + p[3] + ' SUPEQ '

def p_ExpRel_le(p):
    "ExpRel : ExpRel LE ExpA"
    print('ExpRel : ExpRel LE/<= ExpA')
    p[0] = p[1] + p[3] + ' INFEQ '

def p_Exp_add(p):
    "ExpA : ExpA '+' Term"
    print('12')
    p[0] = p[1] + p[3] + ' ADD '

def p_Exp_sub(p):
    "ExpA : ExpA '-' Term"
    print('13')
    p[0] = p[1] + p[3] + ' SUB '

def p_Exp_term(p):
    "ExpA : Term"
    print('14')
    p[0] = p[1]

def p_Term_mul(p):
    "Term : Term '*' Factor"
    print('15')
    p[0] = p[1] + p[3] + ' MUL '

def p_Term_div(p):
    "Term : Term '/' Factor"
    print('16')
    p[0] = p[1] + p[3] + ' DIV '

def p_Term_factor(p):
    "Term : Factor"
    print('17')
    p[0] = p[1]

def p_Factor_id(p):
    "Factor : id"
    print('18')
    p[0] = ' PUSHG ' + str(p.parser.registers.get(p[1])['gp'])

def p_Factor_number(p):
    "Factor : number"
    print('19')
    p[0] = ' PUSHI ' + str(p[1])

def p_Factor_group(p):
    "Factor : '(' ExpA ')'"
    print('20')
    p[0] = p[2]

def p_Factor_array(p):
    "Factor : id '[' number ']'"
    print('21')
    #fazer com o loadn
    p[0] = ' PUSHGP PUSHI ' + str(p.parser.registers.get(p[1])['gp']) + ' PADD PUSHI ' + str(p[3]) + ' LOADN ' 
    #ou
    #p[0] = ' PUSHG ' + str(int((p.parser.registers.get(p[1])['gp']))+int(p[3]))

def p_Factor_true(p):
    "Factor : TRUE"
    print('22')
    p[0] = ' PUSHI 1 '

def p_Factor_false(p):
    "Factor : FALSE"
    print('22')
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
parser.gp = 0           #offset em relacao ao global pointer(gp)
parser.contaIfs = 0
parser.contaCiclos = 0
parser.varscontrolo = {}
for line in sys.stdin:
    parser.parse(line)
