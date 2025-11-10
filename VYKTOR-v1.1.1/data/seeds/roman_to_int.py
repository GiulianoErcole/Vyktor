def solution(s):
    vals = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
    total = 0; prev = 0
    for ch in reversed(s):
        v = vals[ch]
        total = total - v if v < prev else total + v
        prev = v
    return total
def run_tests():
    assert solution("III")==3
    assert solution("IV")==4
    assert solution("IX")==9
    assert solution("LVIII")==58
    assert solution("MCMXCIV")==1994
if __name__=='__main__': run_tests()
