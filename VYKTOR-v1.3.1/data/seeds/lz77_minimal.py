def solution(s, window=20, lookahead=10):
    # Returns list of tuples (offset, length, next_char)
    out=[]; i=0
    while i<len(s):
        best_off=0; best_len=0
        start=max(0, i-window)
        for off in range(i-1, start-1, -1):
            l=0
            while i+l<len(s) and s[off+l]==s[i+l] and l<lookahead:
                l+=1
            if l>best_len:
                best_len=l; best_off=i-off
            if best_len==lookahead: break
        next_char = s[i+best_len] if i+best_len<len(s) else ""
        out.append((best_off,best_len,next_char))
        i += best_len + (1 if next_char else 0)
    return out

def decompress(tokens):
    out=[]
    for off,l,nc in tokens:
        if off==0 and l==0:
            out.append(nc); continue
        start=len(out)-off
        for _ in range(l):
            out.append(out[start]); start+=1
        if nc: out.append(nc)
    return "".join(out)

def run_tests():
    for s in ["", "abc", "aaaaaabaaaab", "banana_bandana_band"]:
        toks=solution(s, window=16, lookahead=8)
        rec=decompress(toks)
        assert rec==s

if __name__=="__main__":
    run_tests()
