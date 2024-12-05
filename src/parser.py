from typing import List

from src.tokens.token import Token
from src.tokens.token_type import TokenType

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_pos = 0
    
    def parse(self):
        # Начало разбора программы
        if not self._match(TokenType.PROGRAM):
            raise SyntaxError("Программа должна начинаться с 'program'")
        
        # Разбор объявления переменных
        if not self._match(TokenType.VAR):
            raise SyntaxError("Ожидается объявление переменных после 'program'")
        
        self._parse_variable_declarations()
        
        # Начало блока операторов
        if not self._match(TokenType.BEGIN):
            raise SyntaxError("Ожидается 'begin' перед началом операторов")
        
        self._parse_statements()
        
        # Конец программы
        if not self._match(TokenType.END):
            raise SyntaxError("Программа должна заканчиваться на 'end.'")
    
    def _parse_variable_declarations(self):
        while not self._check(TokenType.BEGIN):
            # Парсинг списка идентификаторов
            identifiers = []
            while True:
                if not self._check(TokenType.IDENTIFIER):
                    raise SyntaxError("Ожидается идентификатор")
                
                identifiers.append(self._advance())
                
                # Выход из цикла, если нет запятой
                if not self._match(TokenType.COMMA):
                    break
            
            # Ожидание двоеточия и типа
            if not self._match(TokenType.COLON):
                raise SyntaxError("Ожидается ':' после списка идентификаторов")
            
            # Определение типа
            if not self._check_types([TokenType.INTEGER_TYPE, 
                                      TokenType.FLOAT_TYPE, 
                                      TokenType.BOOLEAN_TYPE]):
                raise SyntaxError("Неверный тип данных")
            
            self._advance()  # Пропуск типа
            
            # Ожидание точки с запятой
            if not self._match(TokenType.SEMICOLON):
                raise SyntaxError("Ожидается ';' после объявления типа")
    
    def _parse_statements(self):
        while not self._check(TokenType.END):
            # Разбор оператора
            self._parse_statement()
            
            # Проверка точки с запятой для всех, кроме последнего оператора
            if not self._check_next(TokenType.END) and not self._check(TokenType.END):
                if not self._match(TokenType.SEMICOLON):
                    raise SyntaxError("Требуется точка с запятой между операторами")
            
    
    def _parse_statement(self):
        # Расширим разбор операторов
        if self._check(TokenType.IDENTIFIER):
            self._parse_assignment()
        elif self._check(TokenType.IF):
            self._parse_conditional()
        elif self._check(TokenType.FOR):
            self._parse_fixed_loop()
        elif self._check(TokenType.WHILE):
            self._parse_conditional_loop()
        elif self._check(TokenType.READ):
            self._parse_input()
        elif self._check(TokenType.WRITE):
            self._parse_output()
        else:
            raise SyntaxError("Неожиданный оператор")

    def _parse_assignment(self):
        # Новый синтаксис присваивания с 'as'
        variable = self._advance()  # Идентификатор
        
        if not self._match(TokenType.AS):
            raise SyntaxError("Ожидается 'as' в операторе присваивания")
        
        # Парсинг выражения справа от 'as'
        self._parse_expression()

    def _parse_conditional(self):
        # Условный оператор
        if not self._match(TokenType.IF):
            raise SyntaxError("Ожидается 'if'")
        
        # Условие
        self._parse_expression()
        if not self._match(TokenType.THEN):
            raise SyntaxError(f"Ожидается 'then', получено: {self.tokens[self.current_pos]}")
        
        # Оператор в случае истины
        self._parse_statement()
        
        # Необязательный else
        if self._match(TokenType.ELSE):
            self._parse_statement()

    def _parse_fixed_loop(self):
        # Цикл с фиксированным числом повторений
        if not self._match(TokenType.FOR):
            raise SyntaxError("Ожидается 'for'")
        
        # Начальное присваивание
        self._parse_assignment()
        
        if not self._match(TokenType.TO):
            raise SyntaxError("Ожидается 'to'")
        
        # Выражение завершения цикла
        self._parse_expression()
        
        if not self._match(TokenType.DO):
            raise SyntaxError("Ожидается 'do'")
        
        # Тело цикла
        self._parse_statement()

    def _parse_conditional_loop(self):
        # Условный цикл
        if not self._match(TokenType.WHILE):
            raise SyntaxError("Ожидается 'while'")
        
        # Условие цикла
        self._parse_expression()
        
        if not self._match(TokenType.DO):
            raise SyntaxError("Ожидается 'do'")
        
        # Тело цикла
        self._parse_statement()

    def _parse_input(self):
        # Оператор ввода
        if not self._match(TokenType.READ):
            raise SyntaxError("Ожидается 'read'")
        
        if not self._match(TokenType.LPAREN):
            raise SyntaxError("Ожидается '('")
        
        # Первый идентификатор
        if not self._check(TokenType.IDENTIFIER):
            raise SyntaxError("Ожидается идентификатор")
        
        self._advance()  # Первый идентификатор
        
        # Дополнительные идентификаторы через запятую
        while self._match(TokenType.COMMA):
            if not self._check(TokenType.IDENTIFIER):
                raise SyntaxError("Ожидается идентификатор")
            self._advance()
        
        if not self._match(TokenType.RPAREN):
            raise SyntaxError("Ожидается ')'")

    def _parse_output(self):
        # Оператор вывода
        if not self._match(TokenType.WRITE):
            raise SyntaxError("Ожидается 'write'")
        
        if not self._match(TokenType.LPAREN):
            raise SyntaxError("Ожидается '('")
        
        # Первое выражение
        self._parse_expression()
        
        # Дополнительные выражения через запятую
        while self._match(TokenType.COMMA):
            self._parse_expression()
        
        if not self._match(TokenType.RPAREN):
            raise SyntaxError("Ожидается ')'")
    
    def _parse_compound_statement(self):
        # Составной оператор в квадратных скобках
        if not self._match(TokenType.LPAREN):
            raise SyntaxError("Ожидается '[' в начале составного оператора")
        
        # Разбор операторов внутри составного оператора
        while not self._check(TokenType.RPAREN):
            self._parse_statement()
            # Разрешаем разделители между операторами
            self._match(TokenType.SEMICOLON)
        
        if not self._match(TokenType.RPAREN):
            raise SyntaxError("Ожидается ']' в конце составного оператора")
    
    def _parse_expression(self):
        # Разбор выражения: операнды и операции
        self._parse_operand()
        
        # Поддержка операций отношения
        while self._check_types([
            TokenType.NE, TokenType.EQ, TokenType.LT,
            TokenType.LE, TokenType.GT, TokenType.GE
        ]):
            self._advance()  # Оператор отношения
            self._parse_operand()
    
    def _parse_operand(self):
        # Разбор операнда: слагаемые и операции сложения
        self._parse_summand()
        
        while self._check_types([TokenType.PLUS, TokenType.MIN, TokenType.OR]):
            self._advance()  # Оператор сложения
            self._parse_summand()
    
    def _parse_summand(self):
        # Разбор слагаемого: множители и операции умножения
        self._parse_multiplier()
        
        while self._check_types([TokenType.MULT, TokenType.DIV, TokenType.AND]):
            self._advance()  # Оператор умножения
            self._parse_multiplier()
    
    def _parse_multiplier(self):
        # Разбор множителя: идентификаторы, числа, константы, унарные операции
        if self._check(TokenType.IDENTIFIER):
            self._advance()
        elif self._check(TokenType.INTEGER):
            self._advance()
        elif self._check(TokenType.FLOAT):
            self._advance()
        elif self._check(TokenType.BOOLEAN):
            self._advance()
        elif self._check(TokenType.UNARY_NEGATION):
            self._advance()  # Унарная операция
            self._parse_multiplier()
        elif self._match(TokenType.LPAREN):
            self._parse_expression()
            if not self._match(TokenType.RPAREN):
                raise SyntaxError("Ожидается ')' в конце выражения")
        else:
            raise SyntaxError("Неожиданный множитель в выражении")

    def _match(self, *types) -> bool:
        # Проверка текущего токена и его продвижение
        if self._check(*types):
            self._advance()
            return True
        return False
    
    def _check_next(self, *types) -> bool:
        if self.current_pos + 1 >= len(self.tokens):
            return False
        return self.tokens[self.current_pos + 1].type in types

    def _check(self, *types) -> bool:
        # Проверка текущего токена без продвижения
        if self.current_pos >= len(self.tokens):
            return False
        return self.tokens[self.current_pos].type in types
    
    def _check_types(self, types) -> bool:
        # Проверка типов
        if self.current_pos >= len(self.tokens):
            return False
        return self.tokens[self.current_pos].type in types
    
    def _advance(self) -> Token:
        # Продвижение к следующему токену
        token = self.tokens[self.current_pos]
        self.current_pos += 1
        return token
