FITNESS_PROFILE = { 'accuracy': 0.50, 'efficiency': 0.30, 'entropy': 0.10, 'stability': 0.10 }

def encode(s):
    if not s: return []
    out=[]; cur=s[0]; cnt=1
    for ch in s[1:]:
        if ch==cur: cnt+=1
        else: out.append((cur,cnt)); cur=ch; cnt=1
    out.append((cur,cnt)); return out

def decode(tokens):
    return ''.join(ch*cnt for ch,cnt in tokens)

def solution(s):
    return encode(s)

def fitness_probe():
    s = "aaaaabbbbccccccccccdddeefgggggggggggg"
    toks = encode(s)
    rec = decode(toks)
    cr = len(s)/(len(toks)*2) if toks else 1.0  # naive proxy
    ok = 1.0 if rec==s else 0.0
    return {'ok': ok, 'entropy': 0.5, 'compression_ratio': cr}

def run_tests():
    s = "aaabcccccaaa"
    toks = encode(s)
    assert decode(toks) == s
