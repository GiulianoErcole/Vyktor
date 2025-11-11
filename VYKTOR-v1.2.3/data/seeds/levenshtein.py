def solution(a,b):
    la, lb = len(a), len(b)
    dp = list(range(lb+1))
    for i in range(1, la+1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, lb+1):
            cur = dp[j]
            cost = 0 if a[i-1]==b[j-1] else 1
            dp[j] = min(dp[j]+1, dp[j-1]+1, prev+cost)
            prev = cur
    return dp[lb]

def run_tests():
    assert solution("kitten","sitting")==3
    assert solution("flaw","lawn")==2
    assert solution("","")==0
    assert solution("a","")==1
    assert solution("","abc")==3

if __name__=='__main__': run_tests()
