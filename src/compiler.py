from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from pprint import pprint
class Compiler:
    @staticmethod
    def compile(code: str):
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
            
            return tokens
        
        except SyntaxError as e:
            print(f"Ошибка компиляции: {e}")
            return None
