import math, random

OPS = ['+','-','*']
TERMS = ['x','1','2','-1']

def eval_expr(expr, x):
    stack=[]
    for tok in expr:
        if tok in OPS:
            b=stack.pop(); a=stack.pop()
            if tok=='+': stack.append(a+b)
            elif tok=='-': stack.append(a-b)
            else: stack.append(a*b)
        else:
            if tok=='x': stack.append(x)
            else: stack.append(float(tok))
    return stack[-1]

def rand_expr(max_len=7):
    # simple RPN generator
    expr=[]; depth=0
    for _ in range(max_len):
        if depth<2 or random.random()<0.6:
            expr.append(random.choice(TERMS)); depth+=1
        else:
            expr.append(random.choice(OPS)); depth-=1
    while depth>1:
        expr.append(random.choice(OPS)); depth-=1
    return expr

def loss(expr, xs, ys):
    try:
        err=0.0
        for x,y in zip(xs,ys):
            v=eval_expr(expr,x)
            err+=(v-y)**2
        return err/len(xs)
    except Exception:
        return float('inf')

def solution():
    random.seed(0)
    xs=[-2,-1,0,1,2,3]
    ys=[x*x+x for x in xs]  # target: x^2 + x
    best=None; bestL=float('inf')
    for _ in range(200):
        expr=rand_expr(9)
        L=loss(expr,xs,ys)
        if L<bestL: best,bestL=expr,L
    return best  # RPN tokens

def run_tests():
    expr=solution()
    xs=[-2,-1,0,1,2]
    ys=[x*x+x for x in xs]
    L=loss(expr,xs,ys)
    assert L<1.0  # rough bound

if __name__=="__main__":
    run_tests()
