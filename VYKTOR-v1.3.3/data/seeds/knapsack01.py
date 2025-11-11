def solution(weights, values, W):
    n=len(weights)
    dp=[0]*(W+1)
    for i in range(n):
        w=weights[i]; v=values[i]
        for cap in range(W, w-1, -1):
            dp[cap]=max(dp[cap], dp[cap-w]+v)
    return dp[W]
def run_tests():
    assert solution([2,1,3,2],[12,10,20,15],5)==37
    assert solution([1,2,3],[6,10,12],5)==22
if __name__=='__main__': run_tests()
