import random

def dist2(a,b): return (a[0]-b[0])**2+(a[1]-b[1])**2

def solution(points, k=3, iters=20):
    if not points: return []
    cents=random.sample(points, min(k,len(points)))
    for _ in range(iters):
        clusters=[[] for _ in cents]
        for p in points:
            idx=min(range(len(cents)), key=lambda i: dist2(p,cents[i]))
            clusters[idx].append(p)
        new=[]
        for cl in clusters:
            if cl:
                x=sum(p[0] for p in cl)/len(cl); y=sum(p[1] for p in cl)/len(cl)
                new.append((x,y))
            else:
                new.append(random.choice(points))
        if new==cents: break
        cents=new
    return cents

def run_tests():
    pts=[(0,0),(0.1,0.2),(5,5),(5.2,5.1),(9,9),(9.1,8.8)]
    cents=solution(pts,k=3)
    assert len(cents)==3

if __name__=='__main__':
    run_tests()
