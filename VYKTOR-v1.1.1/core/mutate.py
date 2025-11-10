"""
© 2025 NERON Intelligence Systems — Internal Experimental Research Prototype.
File: mutate.py  |  Module: Vyktor Core  |  Clearance: INTERNAL USE ONLY
"""

import ast, random

class VyktorMutator(ast.NodeTransformer):
    """AST-based mutator: swaps operators, constants, comparisons, loop steps."""
    def visit_BinOp(self, node):
        self.generic_visit(node)
        if random.random() < 0.20:
            node.op = random.choice([ast.Add(), ast.Sub(), ast.Mult(), ast.Div(), ast.Mod()])
        return node

    def visit_Compare(self, node):
        self.generic_visit(node)
        if random.random() < 0.25 and node.ops:
            node.ops[0] = random.choice([ast.Lt(), ast.Gt(), ast.Eq(), ast.NotEq(), ast.LtE(), ast.GtE()])
        return node

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)) and random.random() < 0.15:
            delta = random.randint(-2, 2)
            return ast.copy_location(ast.Constant(node.value + delta), node)
        return node

    def visit_For(self, node):
        self.generic_visit(node)
        # Occasionally adjust range() step to 2 (safe-ish for many tasks)
        if random.random() < 0.10 and isinstance(node.iter, ast.Call) and getattr(node.iter.func, 'id', '') == 'range':
            args = node.iter.args
            if len(args) == 1:
                node.iter.args = [ast.Constant(0), args[0], ast.Constant(2)]
            elif len(args) == 2:
                node.iter.args = [args[0], args[1], ast.Constant(2)]
        return node

def mutate_ast(code: str) -> str:
    """Safely mutate Python code at the AST level (no external deps)."""
    try:
        tree = ast.parse(code)
        VyktorMutator().visit(tree)
        ast.fix_missing_locations(tree)
        try:
            # Python 3.9+: stdlib unparse
            return ast.unparse(tree)  # type: ignore[attr-defined]
        except Exception:
            # If unparse unavailable, return original code to keep zero-dep behavior.
            return code
    except Exception:
        return code
