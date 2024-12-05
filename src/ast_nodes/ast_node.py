from dataclasses import dataclass
from typing import List, Optional
from src.ast_nodes.ast_node_type import NodeType


@dataclass
class ASTNode:
    type: NodeType
    value: Optional[str] = None
    children: List['ASTNode'] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []
