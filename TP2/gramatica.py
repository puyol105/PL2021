g = ''' 
        Limp : BlocoDeclaracoes BEGIN BlocoInstrucoes
       def p_BlocoDeclaracoes(p):
        "BlocoDeclaracoes : Declaracao"
                         | BlocoDeclaracoes Declaracao

        BlocoInstrucoes : Instrucao
                        | BlocoInstrucoes Instrucao

        Declaracao : DeclVar  ';'
                   | DeclArray ';'
                   | DeclArrayBi ';'
                   | DeclFun

        DeclVar : INT id '=' ExpA 
                | INT id
                

        DeclArray : INT id [ number ]

        DeclArrayBi : INT id '[' number ']' '[' number ']' 

        DeclFun : FUNCTION  id '(' ')' '{' BlocoInstrucoes RETURN ExpRel ';' '}'
        
        Instrucao : DUMP ';'
                  | PRINT ExpA ';'
                  | PRINTA ';'
                  | READ id ';'
                  | READ id '[' number ']' ';'
                  | READ id '[' id ']' ';'
                  | Atribuicao ';'
                  | Condicional

        Atribuicao : AtrVar
                   | AtrArray
                   | AtrArrayVar
                   | AtrArrayBi
                   | AtrFun
        
        AtrVar : id '=' ExpA 

        AtrArray : id [ number ] '=' ExpA

        AtrArrayVar : id [ id ] '=' ExpA
        
        AtrArrayBi : id '[' number ']' '[' number ']' '=' ExpA

        AtrFun : id '='  id '(' ')'

        
        Condicional : | IF '(' Condicao ')' '{' BlocoInstrucoes '}' ELSE '{' BlocoInstrucoes '}'
                      | IF '(' Condicao ')' '{' BlocoInstrucoes '}'
                      | REPEAT '{' BlocoInstrucoes '}' 'UNTIL' '(' Condicao ')'
                      | WHILE '(' Condicao ')' DO '{' BlocoInstrucoes '}' 
                      

        (bottom up -> coisas com mais prioridade ficam mais a baixo/direita)
        
        Condicao : ExpLogOr 
        
        ExpLogOr : ExpLogAnd
                 | ExpLogOr OR ExpLogAnd

        ExpLogAnd : ExpLogNot
                  | ExpLogAnd AND ExpLogOr
            
        ExpLogNot : ExpEq
                  | '!' Condicao
        
        ExpEq : ExpRel
              | ExpEq EQ ExpRel
              | ExpEq NE ExpRel
        
        ExpRel : ExpA
              | ExpRel '>' ExpA
              | ExpRel '<' ExpA
              | ExpRel '>=' ExpA
              | ExpRel '<=' ExpA 
         
        ExpA : ExpA '+' Term
             | ExpA '-' Term
             | Term
        
        Term : Term '*' Factor
             | Term '/' Factor
             | Term '%' Factor          X  ???
             | Factor
        
        Factor : id
               | number
               | '(' ExpA ')'
               | id '[' id ']'
               | id '[' number ']'
               | id '[' number ']' '[' number ']' 
               | True
               | False
    '''
