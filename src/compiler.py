from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.ast_builder import ASTBuilder

class Compiler:
    @staticmethod
    def compile(code: str, ast_verbose: bool = False):
        try:
            # Лексический анализ
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            # pprint(tokens)
            print("Лексический анализ завершен.")
            
            # Синтаксический анализ
            parser = Parser(tokens)
            parser.parse()
            print("Синтаксический анализ завершен.")
            
            # Семантический анализ
            semantic_analyzer = SemanticAnalyzer(tokens)
            semantic_analyzer.analyze()
            print("Семантический анализ завершен.")

            ast_builder = ASTBuilder(tokens)
            ast_root = ast_builder.parse()
            if ast_verbose:
                ast_builder.print_ast(ast_root)
            
            return tokens
        
        except SyntaxError as e:
            print(f"Ошибка компиляции: {e}")
            return None
