import math, random

def tour_length(points, tour):
    n=len(tour); L=0.0
    for i in range(n):
        x1,y1=points[tour[i]]
        x2,y2=points[tour[(i+1)%n]]
        L+=math.hypot(x2-x1,y2-y1)
    return L

def solution(points, iters=2000, temp=10.0, alpha=0.995):
    n=len(points)
    tour=list(range(n)); random.shuffle(tour)
    best=tour[:]; bestL=tour_length(points,tour)
    cur=tour[:]; curL=bestL
    for _ in range(iters):
        i,j=sorted(random.sample(range(n),2))
        cand=cur[:]; cand[i:j]=reversed(cand[i:j])
        L=tour_length(points,cand)
        d=L-curL
        if d<0 or random.random()<math.exp(-d/max(1e-9,temp)):
            cur,curL=cand,L
            if curL<bestL: best, bestL = cur[:], curL
        temp*=alpha
    return best

def run_tests():
    pts=[(math.cos(t),math.sin(t)) for t in [i*2*math.pi/12 for i in range(12)]]
    tour=solution(pts, iters=500, temp=5.0)
    assert len(tour)==len(set(tour))==12

if __name__=="__main__":
    run_tests()
