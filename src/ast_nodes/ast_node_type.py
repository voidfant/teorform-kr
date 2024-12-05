from enum import Enum, auto

class NodeType(Enum):
    PROGRAM = auto()
    VARIABLE_DECLARATION = auto()
    ASSIGNMENT = auto()
    CONDITIONAL = auto()
    LOOP = auto()
    INPUT = auto()
    OUTPUT = auto()
    EXPRESSION = auto()
    BINARY_OPERATION = auto()
    UNARY_OPERATION = auto()
    LITERAL = auto()
    IDENTIFIER = auto()