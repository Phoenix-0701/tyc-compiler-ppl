grammar TyC;

options {
    language = Python3;
}

// Lexer error handling

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    t = self.type
    tok = super().emit()
    if t == self.UNCLOSE_STRING:
        raise UncloseString(tok.text[1:])
    elif t == self.ILLEGAL_ESCAPE:
        raise IllegalEscape(tok.text[1:])
    elif t == self.ERROR_CHAR:
        raise ErrorToken(tok.text)
    elif t == self.STRING_LIT:
        tok.text = tok.text[1:-1]
        return tok
    return tok
}

// Parser rules

program
    : unit EOF
    ;

unit
    : declaration*
    ;

declaration
    : structDecl
    | funcDecl
    ;


structDecl
    : STRUCT ID L_BRACE fieldDecl* R_BRACE SEMI
    ;

fieldDecl
    : typeSpec varRef SEMI
    ;


funcDecl
    : returnType? ID L_PAREN paramList? R_PAREN blockStmt
    ;

returnType
    : typeSpec
    | VOID
    | AUTO
    ;

paramList
    : param (COMMA param)*
    ;

param
    : typeSpec varRef
    ;


typeSpec
    : INT
    | FLOAT
    | STRING
    | STRUCT? ID
    ;


stmt
    : varDecl
    | ifStmt
    | whileStmt
    | forStmt
    | switchStmt
    | breakStmt
    | continueStmt
    | returnStmt
    | exprStmt
    | blockStmt
    ;

blockStmt
    : L_BRACE stmt* R_BRACE
    ;

varDecl
    : returnType varInitList SEMI
    ;

varInitList
    : varInit (COMMA varInit)*
    ;

varInit
    : varRef (ASSIGN expr)?
    ;

ifStmt
    : IF L_PAREN expr R_PAREN stmt (ELSE stmt)?
    ;

whileStmt
    : WHILE L_PAREN expr R_PAREN stmt
    ;

forStmt
    : FOR L_PAREN (varDecl | exprStmt | SEMI)
      expr? SEMI expr? R_PAREN stmt
    ;

switchStmt
    : SWITCH L_PAREN expr R_PAREN
      L_BRACE caseStmt* defaultStmt? R_BRACE
    ;

caseStmt
    : CASE expr COLON stmt*
    ;

defaultStmt
    : DEFAULT COLON stmt*
    ;

breakStmt
    : BREAK SEMI
    ;

continueStmt
    : CONTINUE SEMI
    ;

returnStmt
    : RETURN expr? SEMI
    ;

exprStmt
    : expr? SEMI
    ;


expr
    : L_PAREN expr R_PAREN                         # parenExpr
    | expr L_SQUARE expr R_SQUARE                  # arrayExpr
    | expr L_PAREN argList? R_PAREN                # callExpr
    | expr DOT ID                                  # memberExpr
    | expr (INC | DEC)                             # postfixExpr
    | (NOT | ADD | SUB | INC | DEC) expr            # unaryExpr
    | expr (MUL | DIV | MOD) expr                  # mulExpr
    | expr (ADD | SUB) expr                        # addExpr
    | expr (LT | LE | GT | GE) expr                # relExpr
    | expr (EQUAL | NOT_EQUAL) expr                # eqExpr
    | expr AND expr                                # andExpr
    | expr OR expr                                 # orExpr
    | <assoc=right> expr ASSIGN expr               # assignExpr
    | primary                                      # primaryExpr
    ;

primary
    : ID                                           # idExpr
    | INT_LIT                                      # intExpr
    | FLOAT_LIT                                    # floatExpr
    | STRING_LIT                                   # stringExpr
    | L_BRACE argList? R_BRACE                     # structExpr
    ;

argList
    : expr (COMMA expr)*
    ;

varRef
    : ID
    | ID L_SQUARE INT_LIT R_SQUARE
    ;

// Lexer rules

// Keywords
AUTO      : 'auto';
BREAK     : 'break';
CASE      : 'case';
CONTINUE  : 'continue';
DEFAULT   : 'default';
ELSE      : 'else';
FLOAT     : 'float';
FOR       : 'for';
IF        : 'if';
INT       : 'int';
RETURN    : 'return';
STRING    : 'string';
STRUCT    : 'struct';
SWITCH    : 'switch';
VOID      : 'void';
WHILE     : 'while';

// Operators
INC        : '++';
DEC        : '--';
EQUAL      : '==';
NOT_EQUAL  : '!=';
LE         : '<=';
GE         : '>=';
AND        : '&&';
OR         : '||';
ADD        : '+';
SUB        : '-';
MUL        : '*';
DIV        : '/';
MOD        : '%';
LT         : '<';
GT         : '>';
NOT        : '!';
ASSIGN     : '=';
DOT        : '.';
COLON      : ':';
L_SQUARE   : '[';
R_SQUARE   : ']';
L_BRACE    : '{';
R_BRACE    : '}';
L_PAREN    : '(';
R_PAREN    : ')';
SEMI       : ';';
COMMA      : ',';

// Literals
FLOAT_LIT
    : [0-9]+ '.' [0-9]* ([eE] [+-]? [0-9]+)?
    | '.' [0-9]+ ([eE] [+-]? [0-9]+)?
    | [0-9]+ [eE] [+-]? [0-9]+
    ;

INT_LIT : [0-9]+;
ID      : [a-zA-Z_] [a-zA-Z0-9_]*;

STRING_LIT
    : '"' (ESC | ~["\\\r\n])* '"'
    ;

fragment ESC
    : '\\' [bfnrt"\\]
    ;

// Whitespace & comments
WS            : [ \t\r\n\f]+ -> skip;
LINE_COMMENT  : '//' ~[\r\n]* -> skip;
BLOCK_COMMENT : ('/*' .*? '*/' | '/*' (~'*' | '*' ~'/')* ) -> skip;

// Errors
ILLEGAL_ESCAPE
    : '"' (ESC | ~["\\\r\n])* '\\' ~[bfnrt"\\\r\n]
    ;

UNCLOSE_STRING
    : '"' (ESC | ~["\\\r\n])*
    ;

ERROR_CHAR
    : .
    ;
