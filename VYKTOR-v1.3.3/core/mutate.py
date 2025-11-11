import ast, random, json
def _cfg():
    try:
        with open("config.json","r",encoding="utf-8") as f: return json.load(f)
    except Exception: return {}
class VyktorMutator(ast.NodeTransformer):
    def __init__(self, cfg, force_op=None):
        m = cfg.get("mutation", {})
        self.binop_rate=float(m.get("binop_rate",0.20))
        self.compare_rate=float(m.get("compare_rate",0.25))
        self.const_rate=float(m.get("const_rate",0.15))
        self.for_step_rate=float(m.get("for_step_rate",0.10))
        self.delta_min=int(m.get("const_delta_min",-2))
        self.delta_max=int(m.get("const_delta_max",2))
        self.force_op=force_op; self._applied=False
    def _should(self, rate, op):
        if self.force_op: return (not self._applied) and (self.force_op==op)
        return random.random() < rate
    def visit_BinOp(self, node):
        self.generic_visit(node); import ast as A
        if self._should(self.binop_rate,"binop"):
            node.op = random.choice([A.Add(),A.Sub(),A.Mult(),A.Div(),A.Mod()]); self._applied=True
        return node
    def visit_Compare(self, node):
        self.generic_visit(node); import ast as A
        if self._should(self.compare_rate,"compare") and node.ops:
            node.ops[0] = random.choice([A.Lt(),A.Gt(),A.Eq(),A.NotEq(),A.LtE(),A.GtE()]); self._applied=True
        return node
    def visit_Constant(self, node):
        if isinstance(node.value,(int,float)) and self._should(self.const_rate,"const"):
            delta=random.randint(self.delta_min,self.delta_max); import ast as A; self._applied=True
            return A.copy_location(A.Constant(node.value+delta), node)
        return node
    def visit_For(self, node):
        self.generic_visit(node); import ast as A
        if self._should(self.for_step_rate,"for_step") and isinstance(node.iter, A.Call) and getattr(node.iter.func,'id','')=='range':
            args=node.iter.args
            if len(args)==1: node.iter.args=[A.Constant(0), args[0], A.Constant(2)]
            elif len(args)==2: node.iter.args=[args[0], args[1], A.Constant(2)]
            self._applied=True
        return node
def mutate_ast(code: str, cfg=None, force_op=None) -> str:
    cfg = cfg or _cfg(); import ast as A
    try:
        tree=A.parse(code); VyktorMutator(cfg, force_op=force_op).visit(tree); A.fix_missing_locations(tree)
        try: return A.unparse(tree)
        except Exception: return code
    except Exception: return code
