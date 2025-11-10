def solution(xs): return sum(xs)
def run_tests():
    assert solution([1,2,3])==6
    assert solution([])==0
    assert solution([-1,1])==0
if __name__=='__main__': run_tests()
