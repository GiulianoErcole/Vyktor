def solution(samples):
    if not samples: return []
    deltas=[samples[0]]
    for i in range(1,len(samples)):
        deltas.append(samples[i]-samples[i-1])
    return deltas

def reconstruct(deltas):
    if not deltas: return []
    out=[deltas[0]]
    for i in range(1,len(deltas)):
        out.append(out[-1]+deltas[i])
    return out

def run_tests():
    s=[0,1,3,6,10,15,15,14,10]
    d=solution(s)
    assert reconstruct(d)==s
    assert sum(abs(x) for x in d) < sum(abs(x) for x in s)  # crude compression proxy

if __name__=='__main__':
    run_tests()
