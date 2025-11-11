import random

def _hashes(item, m, k):
    r=random.Random(hash(item) & 0xffffffff)
    for _ in range(k):
        yield r.randrange(m)

class Bloom:
    def __init__(self, m=256, k=3):
        self.m=m; self.k=k; self.bits=[0]*m
    def add(self, item):
        for h in _hashes(item, self.m, self.k): self.bits[h]=1
    def __contains__(self, item):
        return all(self.bits[h]==1 for h in _hashes(item, self.m, self.k))

def solution(items, queries):
    bf=Bloom(m=256,k=3)
    for it in items: bf.add(it)
    return [q in bf for q in queries]

def run_tests():
    items=[f"word{i}" for i in range(100)]
    queries=items[:10]+["not_in"]
    res=solution(items,queries)
    assert all(res[:10]) and (res[-1] in [False, True])  # may false-positive

if __name__=='__main__':
    run_tests()
