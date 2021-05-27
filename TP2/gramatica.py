g = ''' 
        Limp : BlocoDeclaracoes BEGIN BlocoInstrucoes

        BlocoDeclaracoes : Declaracao
                         | BlocoDeclaracoes Declaracao

        BlocoInstrucoes : Instrucao
                        | BlocoInstrucoes Instrucao

        Declaracao : DeclVar  ';'
                   | DeclArray ';'
                   | DeclFun

        DeclVar : INT id '=' ExpA 
                | INT id

        DeclArray : INT id [ number ]

        DeclFun : empty
        
        Instrucao : DUMP ';'
                  | PRINT ExpA ';'    pode dar print Exp
                  | PRINTA ';'
                  | READ id ';'
                  | READ id '[' number ']' ';'
                  | Atribuicao ';'
                  | Condicional

        Atribuicao : AtrVar
                   | AtrArray
        
        AtrVar : id '=' ExpA

        AtrArray : id [ number ] '=' ExpA
        
        Condicional : | IF ( Condicao ) { BlocoInstrucoes } ELSE { BlocoInstrucoes }
                      | IF ( Condicao ) { BlocoInstrucoes }
                      | WHILE (Condicao) { BlocoInstrucoes }

        (bottom up -> coisas com mais prioridade ficam mais a baixo/direita)
        
        Cond : Cond OR Cond2
             | Cond2
        
        Cond2: Cond2 AND Cond3
             | Cond3
        
        Cond3 : NOT Cond
             | ExpRel
        
          X?  ExpRel : Exp '>'Exp'
          X     ...
          X     | Exp
        
          X | ExpA                   Aritmetica
          X | ExpL  AND OR NOT       Logica
          X | ExpR                   Relacional

        ExpA : ExpA '+' Term
             | ExpA '-' Term
             | Term
        
        Term : Term '*' Factor
             | Term '/' Factor
             | Term '%' Factor    X
             | Factor
        
        Factor : id
               | number"
               | '(' ExpA ')'
               | id [ number ]
        
        Condicao: ExpRel

        ExpRel : ExpA
               | ExpRel '>' ExpA
               | ExpRel '<' ExpA
               | ExpRel '>=' ExpA
               | ExpRel '<=' ExpA

    '''
