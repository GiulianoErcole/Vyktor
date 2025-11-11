def solution(n):
    if n<2: return False
    for i in range(2,int(n**0.5)+1):
        if n%i==0: return False
    return True
def run_tests():
    assert solution(2); assert solution(3)
    assert not solution(1); assert not solution(4)
    assert solution(13)
if __name__=='__main__': run_tests()
