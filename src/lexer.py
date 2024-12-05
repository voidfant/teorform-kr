import re

from typing import List

from src.tokens.token import Token
from src.tokens.token_type import TokenType

class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.tokens: List[Token] = []
        self.current_pos = 0
    
    def tokenize(self) -> List[Token]:
        while self.current_pos < len(self.code):
            char = self.code[self.current_pos]
            
            if char == '{':
                self._handle_multiline_comment()
                continue

            # Пропуск пробелов
            if char.isspace():
                self.current_pos += 1
                continue
            
            # Типы данных
            if char in ['%', '!', '$']:
                self._handle_data_type(char)
                continue
            
            # Операторы и символы
            if self._handle_operators():
                continue
            
            # Идентификаторы и ключевые слова
            if char.isalpha():
                self._handle_identifier()
                continue
            
            # Числа
            if char.isdigit():
                self._handle_number()
                continue
            
            
            # Неизвестный символ
            raise SyntaxError(f"Неожиданный символ: {char}")
        
        return self.tokens
    
    def _handle_multiline_comment(self):
        # Пропуск многострочного комментария
        self.current_pos += 1
        while self.current_pos < len(self.code):
            if self.code[self.current_pos] == '}':
                self.current_pos += 1
                break
            self.current_pos += 1

    def _handle_data_type(self, type_char: str):
        # Добавление токена типа данных
        type_map = {
            '%': TokenType.INTEGER_TYPE,
            '!': TokenType.FLOAT_TYPE,
            '$': TokenType.BOOLEAN_TYPE
        }
        
        self.tokens.append(Token(type_map[type_char], type_char))
        self.current_pos += 1

    def _handle_identifier(self):
        start = self.current_pos
        while (self.current_pos < len(self.code) and
               (self.code[self.current_pos].isalpha() or
                self.code[self.current_pos].isdigit() or
                self.code[self.current_pos] == '.')):
            self.current_pos += 1
        
        value = self.code[start:self.current_pos]
        
        keywords = {
            # Существующие ключевые слова
            'program': TokenType.PROGRAM,
            'var': TokenType.VAR,
            'begin': TokenType.BEGIN,
            'end.': TokenType.END,
            'true': TokenType.BOOLEAN,
            'false': TokenType.BOOLEAN,
            'as': TokenType.AS,
            'if': TokenType.IF,
            'then': TokenType.THEN,
            'else': TokenType.ELSE,
            'for': TokenType.FOR,
            'to': TokenType.TO,
            'do': TokenType.DO,
            'while': TokenType.WHILE,
            'read': TokenType.READ,
            'write': TokenType.WRITE
        }
        
        token_type = keywords.get(value, TokenType.IDENTIFIER)
        self.tokens.append(Token(token_type, value))
    
    def _handle_number(self):
        # Обработка различных форматов чисел
        start = self.current_pos
        while (self.current_pos < len(self.code) and
               (self.code[self.current_pos].isdigit() or
                self.code[self.current_pos] in 'ABCDEFabcdefHhOoBbDd.')):
            self.current_pos += 1
        
        value = self.code[start:self.current_pos]
        
        # Определение типа числа
        if re.match(r'^[01]+[Bb]$', value):
            self.tokens.append(Token(TokenType.INTEGER, value))
        elif re.match(r'^[0-7]+[Oo]$', value):
            self.tokens.append(Token(TokenType.INTEGER, value))
        elif re.match(r'^\d+[Dd]?$', value):
            self.tokens.append(Token(TokenType.INTEGER, value))
        elif re.match(r'^\d*\.\d+([Ee][+-]?\d+)?$', value) or \
             re.match(r'^\d+\.\d*([Ee][+-]?\d+)?$', value):
            self.tokens.append(Token(TokenType.FLOAT, value))
        elif re.match(r'^[\dA-Fa-f]+[Hh]$', value):
            self.tokens.append(Token(TokenType.INTEGER, value))
        else:
            raise SyntaxError(f"Неверный формат числа: {value}")
    
    def _handle_operators(self) -> bool:
        operators = {
            '~': TokenType.UNARY_NEGATION,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            ';': TokenType.SEMICOLON,
            ':': TokenType.COLON,
            ',': TokenType.COMMA
        }
        
        complex_operators = {
            'NE': TokenType.NE,
            'EQ': TokenType.EQ,
            'LT': TokenType.LT,
            'LE': TokenType.LE,
            'GT': TokenType.GT,
            'GE': TokenType.GE,
            'plus': TokenType.PLUS,
            'min': TokenType.MIN,
            'or': TokenType.OR,
            'mult': TokenType.MULT,
            'div': TokenType.DIV,
            'and': TokenType.AND
        }
        
        # Простые операторы
        if self.code[self.current_pos] in operators:
            self.tokens.append(Token(operators[self.code[self.current_pos]],
                                     self.code[self.current_pos]))
            self.current_pos += 1
            return True
        
        # Сложные операторы
        for op, token_type in complex_operators.items():
            if self.code[self.current_pos:].startswith(op):
                self.tokens.append(Token(token_type, op))
                self.current_pos += len(op)
                return True
        print('не нашел')
        return False
