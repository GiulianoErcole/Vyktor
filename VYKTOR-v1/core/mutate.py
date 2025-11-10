"""
© 2025 NERON Intelligence Systems — Internal Experimental Research Prototype.
File: mutate.py  |  Module: Vyktor Core  |  Clearance: INTERNAL USE ONLY
"""

import ast, astor, random

class VyktorMutator(ast.NodeTransformer):
    def visit_BinOp(self, node):
        self.generic_visit(node)
        if random.random() < 0.2:
            node.op = random.choice([ast.Add(), ast.Sub(), ast.Mult(), ast.Div(), ast.Mod()])
        return node

    def visit_Compare(self, node):
        self.generic_visit(node)
        if random.random() < 0.25 and node.ops:
            node.ops[0] = random.choice([ast.Lt(), ast.Gt(), ast.Eq(), ast.NotEq()])
        return node

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)) and random.random() < 0.15:
            return ast.Constant(node.value + random.randint(-2, 2))
        return node

def mutate_ast(code: str) -> str:
    try:
        tree = ast.parse(code)
        VyktorMutator().visit(tree)
        ast.fix_missing_locations(tree)
        return astor.to_source(tree)
    except Exception:
        return code
