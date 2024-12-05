from typing import List, Dict, Optional, Set
from pprint import pprint
from src.tokens.token import Token
from src.tokens.token_type import TokenType

class SemanticAnalyzer:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.symbol_table: Dict[str, TokenType] = {}
        self.type_compatibility: Dict[TokenType, Set[TokenType]] = {
            TokenType.INTEGER: {TokenType.INTEGER},
            TokenType.FLOAT: {TokenType.FLOAT, TokenType.INTEGER},
            TokenType.BOOLEAN: {TokenType.BOOLEAN}
        }
        self.operator_type_rules = {
            # Правила для операций сложения
            TokenType.PLUS: {
                'left_types': {TokenType.INTEGER, TokenType.FLOAT},
                'right_types': {TokenType.INTEGER, TokenType.FLOAT},
                'result_type': TokenType.INTEGER
            },
            TokenType.MIN: {
                'left_types': {TokenType.INTEGER, TokenType.FLOAT},
                'right_types': {TokenType.INTEGER, TokenType.FLOAT},
                'result_type': TokenType.INTEGER
            },
            # Правила для операций отношения
            TokenType.LT: {
                'left_types': {TokenType.INTEGER, TokenType.FLOAT},
                'right_types': {TokenType.INTEGER, TokenType.FLOAT},
                'result_type': TokenType.BOOLEAN
            },
            TokenType.GT: {
                'left_types': {TokenType.INTEGER, TokenType.FLOAT},
                'right_types': {TokenType.INTEGER, TokenType.FLOAT},
                'result_type': TokenType.BOOLEAN
            }
        }
    
    def analyze(self):
        # Регистрация переменных с учетом блока объявлений
        self._register_variables()
        
        # Проверка типов и семантики выражений
        self._check_type_consistency()
    
    def _register_variables(self):
        # Заполнение таблицы символов с более надежным парсингом
        current_pos = 0
        while current_pos < len(self.tokens):
            if self.tokens[current_pos].type == TokenType.VAR:
                current_pos += 1
                while (current_pos < len(self.tokens) and
                       self.tokens[current_pos].type != TokenType.BEGIN):
                    # Группировка идентификаторов одного типа
                    identifiers = []
                    while (current_pos < len(self.tokens) and
                           self.tokens[current_pos].type in (TokenType.IDENTIFIER, TokenType.COMMA)):
                        if self.tokens[current_pos].type != TokenType.COMMA:
                            identifiers.append(self.tokens[current_pos].value)
                        current_pos += 1
                    
                    # Пропуск двоеточия
                    if self.tokens[current_pos].type == TokenType.COLON:
                        current_pos += 1
                    
                    # Определение типа
                    if current_pos < len(self.tokens):
                        var_type = self._map_type_symbol(self.tokens[current_pos].type)
                        
                        # Регистрация переменных с одинаковым типом
                        for identifier in identifiers:
                            self.symbol_table[identifier] = var_type
                    
                    current_pos += 1
            current_pos += 1
    
    def _map_type_symbol(self, token_type: TokenType) -> TokenType:
        """Маппинг символов типов к внутренним типам"""
        type_mapping = {
            TokenType.INTEGER_TYPE: TokenType.INTEGER,
            TokenType.FLOAT_TYPE: TokenType.FLOAT,
            TokenType.BOOLEAN_TYPE: TokenType.BOOLEAN
        }
        return type_mapping.get(token_type, TokenType.FLOAT)  # По умолчанию FLOAT
    
    def get_variable_type(self, identifier: str) -> Optional[TokenType]:
        return self.symbol_table.get(identifier)
    
    def _check_type_consistency(self):
        # Проверка семантической корректности
        i = 0
        while i < len(self.tokens):
            # Проверка присваивания
            if self.tokens[i].type == TokenType.AS:
                self._validate_assignment(i)
            
            # Проверка операций
            elif self.tokens[i].type in {TokenType.PLUS, TokenType.MIN, 
                                         TokenType.LT, TokenType.GT}:
                self._validate_operation(i)
            
            i += 1
    
    def _validate_assignment(self, as_pos: int):
        # Левый операнд (переменная)
        left_token = self.tokens[as_pos - 1]
        # Правый операнд (значение)
        right_token = self.tokens[as_pos + 1]
        
        # Получаем тип левой переменной
        left_type = self.get_variable_type(left_token.value)
        
        if left_type is None:
            raise SyntaxError(f"Необъявленная переменная: {left_token.value}")
        
        # Определение типа правого выражения
        right_type = None
        if right_token.type == TokenType.IDENTIFIER:
            right_type = self.get_variable_type(right_token.value)
        elif right_token.type in {TokenType.INTEGER, TokenType.FLOAT, TokenType.BOOLEAN}:
            right_type = right_token.type
        
        if right_type is None:
            raise SyntaxError(f"Невозможно определить тип: {right_token.value}")
        
        # Проверка совместимости типов
        if not self._are_types_compatible(left_type, right_type):
            pprint(self.symbol_table)
            raise SyntaxError(f"Несовместимые типы при присваивании: {left_type} ≠ {right_type} ({left_token.value} {right_token.value})")
    
    def _validate_operation(self, op_pos: int):
        # Получаем операцию
        operation = self.tokens[op_pos]
        
        # Левый операнд
        left_token = self.tokens[op_pos - 1]
        # Правый операнд
        right_token = self.tokens[op_pos + 1]
        
        # Определение типов
        left_type = (self.get_variable_type(left_token.value) 
                     if left_token.type == TokenType.IDENTIFIER 
                     else left_token.type)
        
        right_type = (self.get_variable_type(right_token.value) 
                      if right_token.type == TokenType.IDENTIFIER 
                      else right_token.type)
        
        # Проверка операции по правилам
        op_rules = self.operator_type_rules.get(operation.type)
        if op_rules:
            # Проверка типов левого операнда
            if left_type not in op_rules['left_types']:
                raise SyntaxError(f"Недопустимый тип левого операнда для {operation.type}")
            
            # Проверка типов правого операнда
            if right_type not in op_rules['right_types']:
                raise SyntaxError(f"Недопустимый тип правого операнда для {operation.type}")
    
    def _are_types_compatible(self, type1: TokenType, type2: TokenType) -> bool:
        """Проверка совместимости типов"""
        return type2 in self.type_compatibility.get(type1, set())