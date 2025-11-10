def solution(s): return s[::-1]

def run_tests():
    assert solution('abc')=='cba'
    assert solution('')==''
    assert solution('12345')=='54321'

if __name__=='__main__': run_tests()
