from src.tokens.token_type import TokenType

class Token:
    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return f"Token({self.type}, {self.value})"
