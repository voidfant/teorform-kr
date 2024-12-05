from enum import Enum

class TokenType(Enum):
    # Операции отношения
    NE = 'NE'  # !=
    EQ = 'EQ'  # ==
    LT = 'LT'  # <
    LE = 'LE'  # <=
    GT = 'GT'  # >
    GE = 'GE'  # >=
    
    # Операции сложения
    PLUS = 'plus'
    MIN = 'min'
    OR = 'or'
    
    # Операции умножения
    MULT = 'mult'
    DIV = 'div'
    AND = 'and'
    
    # Унарная операция
    UNARY_NEGATION = '~'
    
    # Идентификаторы и константы
    IDENTIFIER = 'IDENTIFIER'
    INTEGER = 'INTEGER'
    FLOAT = 'FLOAT'
    BOOLEAN = 'BOOLEAN'
    
    # Служебные символы
    LPAREN = '('
    RPAREN = ')'
    SEMICOLON = ';'
    COLON = ':'
    COMMA = ','
    
    # Ключевые слова
    PROGRAM = 'program'
    VAR = 'var'
    BEGIN = 'begin'
    END = 'end.'
    
    # Типы данных
    INTEGER_TYPE = '%'
    FLOAT_TYPE = '!'
    BOOLEAN_TYPE = '$'

    AS = 'as'
    IF = 'if'
    THEN = 'then'
    ELSE = 'else'
    FOR = 'for'
    TO = 'to'
    DO = 'do'
    WHILE = 'while'
    READ = 'read'
    WRITE = 'write'
    COMMENT_START = '{'
    COMMENT_END = '}'
