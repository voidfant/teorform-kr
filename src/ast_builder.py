from src.ast_nodes.ast_node_type import NodeType
from src.ast_nodes.ast_node import ASTNode

from src.tokens.token import Token
from src.tokens.token_type import TokenType

from src.parser import Parser

from typing import List, Optional


class ASTBuilder(Parser):
    def __init__(self, tokens: List[Token]):
        super().__init__(tokens)
        self.root = None

    def parse(self):
        self.root = ASTNode(NodeType.PROGRAM)
        
        # Пропускаем 'program'
        self._match(TokenType.PROGRAM)
        
        # Пропускаем 'var'
        self._match(TokenType.VAR)
        
        # Добавляем объявления переменных
        var_declarations = self._build_variable_declarations()
        self.root.children.extend(var_declarations)
        
        # Пропускаем 'begin'
        self._match(TokenType.BEGIN)
        
        # Добавляем операторы
        statements = self._build_statements()
        self.root.children.extend(statements)
        
        # Пропускаем 'end'
        self._match(TokenType.END)
        
        return self.root

    def _build_variable_declarations(self) -> List[ASTNode]:
        declarations = []
        
        while not self._check(TokenType.BEGIN):
            identifiers = []
            while True:
                if not self._check(TokenType.IDENTIFIER):
                    break
                
                identifiers.append(self._advance().value)
                
                if not self._match(TokenType.COMMA):
                    break
            
            # Пропускаем двоеточие
            self._match(TokenType.COLON)
            
            # Получаем тип
            var_type = self._advance().type
            
            # Создаем узел объявления переменных
            for identifier in identifiers:
                decl_node = ASTNode(
                    type=NodeType.VARIABLE_DECLARATION, 
                    value=identifier,
                    children=[ASTNode(type=NodeType.IDENTIFIER, value=str(var_type))]
                )
                declarations.append(decl_node)
            
            # Пропускаем точку с запятой
            self._match(TokenType.SEMICOLON)
        
        return declarations

    def _build_statements(self) -> List[ASTNode]:
        statements = []
        
        while not self._check(TokenType.END):
            statement = self._build_statement()
            if statement:
                statements.append(statement)
            
            # Необязательная точка с запятой между операторами
            self._match(TokenType.SEMICOLON)
        
        return statements

    def _build_statement(self) -> Optional[ASTNode]:
        if self._check(TokenType.IDENTIFIER):
            return self._build_assignment()
        elif self._check(TokenType.IF):
            return self._build_conditional()
        elif self._check(TokenType.FOR):
            return self._build_fixed_loop()
        elif self._check(TokenType.WHILE):
            return self._build_conditional_loop()
        elif self._check(TokenType.READ):
            return self._build_input()
        elif self._check(TokenType.WRITE):
            return self._build_output()
        
        return None

    def _build_assignment(self) -> ASTNode:
        variable = self._advance().value
        
        # Пропускаем 'as'
        self._match(TokenType.AS)
        
        # Разбираем выражение
        expression = self._build_expression()
        
        return ASTNode(
            type=NodeType.ASSIGNMENT,
            value=variable,
            children=[expression]
        )

    def _build_expression(self) -> ASTNode:
        left_operand = self._build_operand()
        
        # Проверяем операции отношения
        while self._check_types([
            TokenType.NE, TokenType.EQ, TokenType.LT,
            TokenType.LE, TokenType.GT, TokenType.GE
        ]):
            operator = self._advance().type
            right_operand = self._build_operand()
            
            left_operand = ASTNode(
                type=NodeType.BINARY_OPERATION,
                value=str(operator),
                children=[left_operand, right_operand]
            )
        
        return left_operand

    def _build_operand(self) -> ASTNode:
        left_summand = self._build_summand()
        
        while self._check_types([TokenType.PLUS, TokenType.MIN, TokenType.OR]):
            operator = self._advance().type
            right_summand = self._build_summand()
            
            left_summand = ASTNode(
                type=NodeType.BINARY_OPERATION,
                value=str(operator),
                children=[left_summand, right_summand]
            )
        
        return left_summand

    def _build_conditional(self) -> ASTNode:
        # Пропускаем 'if'
        self._match(TokenType.IF)
        
        # Разбираем условие
        condition = self._build_expression()
        
        # Пропускаем 'then'
        self._match(TokenType.THEN)
        
        # Разбираем оператор в случае истины
        true_branch = self._build_statement()
        
        # Необязательный else
        false_branch = None
        if self._match(TokenType.ELSE):
            false_branch = self._build_statement()
        
        return ASTNode(
            type=NodeType.CONDITIONAL,
            children=[condition, true_branch, false_branch] if false_branch else [condition, true_branch]
        )

    def _build_fixed_loop(self) -> ASTNode:
        # Пропускаем 'for'
        self._match(TokenType.FOR)
        
        # Начальное присваивание
        initial_assignment = self._build_assignment()
        
        # Пропускаем 'to'
        self._match(TokenType.TO)
        
        # Разбираем выражение завершения цикла
        end_condition = self._build_expression()
        
        # Пропускаем 'do'
        self._match(TokenType.DO)
        
        # Разбираем тело цикла
        loop_body = self._build_statement()
        
        return ASTNode(
            type=NodeType.LOOP,
            value='for',
            children=[initial_assignment, end_condition, loop_body]
        )

    def _build_conditional_loop(self) -> ASTNode:
        # Пропускаем 'while'
        self._match(TokenType.WHILE)
        
        # Разбираем условие цикла
        condition = self._build_expression()
        
        # Пропускаем 'do'
        self._match(TokenType.DO)
        
        # Разбираем тело цикла
        loop_body = self._build_statement()
        
        return ASTNode(
            type=NodeType.LOOP,
            value='while',
            children=[condition, loop_body]
        )

    def _build_input(self) -> ASTNode:
        # Пропускаем 'read'
        self._match(TokenType.READ)
        
        # Пропускаем '('
        self._match(TokenType.LPAREN)
        
        # Список переменных для ввода
        input_vars = []
        
        while True:
            if not self._check(TokenType.IDENTIFIER):
                break
            
            input_vars.append(ASTNode(
                type=NodeType.IDENTIFIER, 
                value=self._advance().value
            ))
            
            if not self._match(TokenType.COMMA):
                break
        
        # Пропускаем ')'
        self._match(TokenType.RPAREN)
        
        return ASTNode(
            type=NodeType.INPUT,
            children=input_vars
        )

    def _build_output(self) -> ASTNode:
        # Пропускаем 'write'
        self._match(TokenType.WRITE)
        
        # Пропускаем '('
        self._match(TokenType.LPAREN)
        
        # Список выражений для вывода
        output_expressions = []
        
        while True:
            output_expressions.append(self._build_expression())
            
            if not self._match(TokenType.COMMA):
                break
        
        # Пропускаем ')'
        self._match(TokenType.RPAREN)
        
        return ASTNode(
            type=NodeType.OUTPUT,
            children=output_expressions
        )

    def _build_summand(self) -> ASTNode:
        left_multiplier = self._build_multiplier()
        
        while self._check_types([TokenType.MULT, TokenType.DIV, TokenType.AND]):
            operator = self._advance().type
            right_multiplier = self._build_multiplier()
            
            left_multiplier = ASTNode(
                type=NodeType.BINARY_OPERATION,
                value=str(operator),
                children=[left_multiplier, right_multiplier]
            )
        
        return left_multiplier

    def _build_multiplier(self) -> ASTNode:
        if self._check(TokenType.IDENTIFIER):
            return ASTNode(
                type=NodeType.IDENTIFIER, 
                value=self._advance().value
            )
        elif self._check(TokenType.INTEGER):
            return ASTNode(
                type=NodeType.LITERAL, 
                value=self._advance().value,
                children=[ASTNode(type=NodeType.IDENTIFIER, value='integer')]
            )
        elif self._check(TokenType.FLOAT):
            return ASTNode(
                type=NodeType.LITERAL, 
                value=self._advance().value,
                children=[ASTNode(type=NodeType.IDENTIFIER, value='float')]
            )
        elif self._check(TokenType.BOOLEAN):
            return ASTNode(
                type=NodeType.LITERAL, 
                value=self._advance().value,
                children=[ASTNode(type=NodeType.IDENTIFIER, value='boolean')]
            )
        elif self._check(TokenType.UNARY_NEGATION):
            operator = self._advance().type
            operand = self._build_multiplier()
            
            return ASTNode(
                type=NodeType.UNARY_OPERATION,
                value=str(operator),
                children=[operand]
            )
        elif self._match(TokenType.LPAREN):
            expression = self._build_expression()
            
            # Пропускаем ')'
            self._match(TokenType.RPAREN)
            
            return expression
        else:
            raise SyntaxError("Неожиданный множитель в выражении")
    
    def print_ast(self, node: ASTNode, level: int = 0):
        """Вспомогательный метод для печати дерева"""
        indent = "  " * level
        print(f"{indent}{node.type.name}: {node.value if node.value is not None else ''}")
        
        for child in node.children:
            self.print_ast(child, level + 1)
