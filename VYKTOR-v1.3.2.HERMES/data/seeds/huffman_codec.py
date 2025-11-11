from heapq import heappush, heappop

class Node:
    __slots__ = ("freq","ch","l","r")
    def __init__(self,freq,ch=None,l=None,r=None):
        self.freq=freq; self.ch=ch; self.l=l; self.r=r
    def __lt__(self,other): return self.freq<other.freq

def _build_tree(freqs):
    heap=[]
    for ch,f in freqs.items(): heappush(heap, Node(f,ch))
    if not heap: return None
    if len(heap)==1:
        # single char: add a dummy
        only=heappop(heap); return Node(only.freq, None, only, Node(0,'\0'))
    while len(heap)>1:
        a=heappop(heap); b=heappop(heap)
        heappush(heap, Node(a.freq+b.freq,None,a,b))
    return heappop(heap)

def _codes(root, path="", table=None):
    if table is None: table={}
    if not root: return table
    if root.ch is not None:
        table[root.ch]=path or "0"
    else:
        _codes(root.l, path+"0", table)
        _codes(root.r, path+"1", table)
    return table

def solution(text):
    # returns (bitstring, codebook) and provides a decode helper
    from collections import Counter
    freqs=Counter(text)
    root=_build_tree(freqs)
    code=_codes(root)
    bits="".join(code[ch] for ch in text)
    return bits, code

def decode(bits, code):
    rev={v:k for k,v in code.items()}
    out=[]; buf=""
    for b in bits:
        buf+=b
        if buf in rev:
            out.append(rev[buf]); buf=""
    if buf: raise ValueError("dangling bits")
    return "".join(out)

def run_tests():
    for s in ["", "aaaaa", "abracadabra", "the quick brown fox jumps over the lazy dog"]:
        bits,code=solution(s)
        assert decode(bits, code)==s
    # codes must be prefix-free (simple spot check)
    bits,code=solution("aabbbc")
    for k1,v1 in code.items():
        for k2,v2 in code.items():
            if k1!=k2:
                assert not v2.startswith(v1), "prefix violation"

if __name__=="__main__":
    run_tests()
