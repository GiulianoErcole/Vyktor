import heapq
def solution(n, edges, src):
    g=[[] for _ in range(n)]
    for u,v,w in edges:
        g[u].append((v,w)); g[v].append((u,w))
    INF=10**18; dist=[INF]*n; dist[src]=0
    pq=[(0,src)]
    while pq:
        d,u=heapq.heappop(pq)
        if d!=dist[u]: continue
        for v,w in g[u]:
            nd=d+w
            if nd<dist[v]:
                dist[v]=nd; heapq.heappush(pq,(nd,v))
    return dist
def run_tests():
    n=5; edges=[(0,1,2),(1,2,3),(0,3,1),(3,2,1),(2,4,5)]
    assert solution(n,edges,0)==[0,2,2,1,7]
if __name__=='__main__': run_tests()
