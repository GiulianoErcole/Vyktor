import random

def contract(edges, n):
    parent=list(range(n))
    def find(a):
        while parent[a]!=a:
            parent[a]=parent[parent[a]]
            a=parent[a]
        return a
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: parent[rb]=ra
    remaining=n
    E=edges[:]
    while remaining>2:
        u,v=random.choice(E)
        ru,rv=find(u),find(v)
        if ru==rv: continue
        union(ru,rv); remaining-=1
        # merge edges
        newE=[]
        for a,b in E:
            ra,rb=find(a),find(b)
            if ra!=rb: newE.append((ra,rb))
        E=newE
    cut=0
    for a,b in edges:
        if find(a)!=find(b): cut+=1
    return cut

def solution(n, edges, trials=10):
    best=float('inf')
    for _ in range(trials):
        c=contract(edges, n)
        if c<best: best=c
    return best

def run_tests():
    # triangle has min cut 2
    n=3; edges=[(0,1),(1,2),(0,2)]
    assert solution(n, edges, trials=5)==2

if __name__=='__main__':
    run_tests()
