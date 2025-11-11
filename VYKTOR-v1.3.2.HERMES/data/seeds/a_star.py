from heapq import heappush, heappop
def heuristic(a,b): return abs(a[0]-b[0])+abs(a[1]-b[1])
def neighbors(x,y,w,h):
    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        nx,ny=x+dx,y+dy
        if 0<=nx<w and 0<=ny<h: yield nx,ny
def solution(grid, start, goal):
    w,h=len(grid[0]),len(grid)
    open=[]; heappush(open,(0,start)); g={start:0}; came={}
    while open:
        _,cur=heappop(open)
        if cur==goal: break
        x,y=cur
        for nx,ny in neighbors(x,y,w,h):
            cost=grid[ny][nx]
            ng=g[cur]+cost
            if (nx,ny) not in g or ng<g[(nx,ny)]:
                g[(nx,ny)]=ng
                f=ng+heuristic((nx,ny),goal)
                heappush(open,(f,(nx,ny)))
                came[(nx,ny)]=cur
    path=[]; cur=goal
    while cur!=start and cur in came:
        path.append(cur); cur=came[cur]
    path.append(start); path.reverse()
    return path
def run_tests():
    grid=[[1,1,1],[9,1,9],[1,1,1]]
    p=solution(grid,(0,0),(2,2))
    assert p[0]==(0,0) and p[-1]==(2,2) and len(p)>=3
if __name__=='__main__': run_tests()
