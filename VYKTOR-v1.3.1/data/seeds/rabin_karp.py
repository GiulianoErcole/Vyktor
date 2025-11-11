def solution(text, pattern):
    if pattern=="": return 0
    n=len(text); m=len(pattern)
    if m>n: return -1
    base=256; mod=2_000_003
    hp=0; ht=0; powb=1
    for i in range(m):
        hp=(hp*base+ord(pattern[i]))%mod
        ht=(ht*base+ord(text[i]))%mod
        if i<m-1: powb=(powb*base)%mod
    for i in range(n-m+1):
        if hp==ht and text[i:i+m]==pattern:
            return i
        if i<n-m:
            ht = ( (ht - ord(text[i])*powb)*base + ord(text[i+m]) ) % mod
            if ht<0: ht+=mod
    return -1

def run_tests():
    assert solution("hello world","world")==6
    assert solution("aaaaa","b")==-1
    assert solution("","")==0

if __name__=='__main__':
    run_tests()
