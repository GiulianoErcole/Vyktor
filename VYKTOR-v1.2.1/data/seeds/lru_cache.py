class LRU:
    def __init__(self, cap):
        self.cap = cap
        self.d = {}
        self.order = []
    def get(self, k):
        if k not in self.d: return -1
        self.order.remove(k); self.order.append(k)
        return self.d[k]
    def put(self, k, v):
        if k in self.d:
            self.d[k] = v
            self.order.remove(k); self.order.append(k)
        else:
            if len(self.d) >= self.cap:
                old = self.order.pop(0)
                del self.d[old]
            self.d[k] = v; self.order.append(k)

def solution(_):
    return "OK"

def run_tests():
    c = LRU(2)
    c.put(1,1); c.put(2,2); assert c.get(1)==1
    c.put(3,3); assert c.get(2)==-1
    c.put(4,4); assert c.get(1)==-1
    assert c.get(3)==3 and c.get(4)==4

if __name__=='__main__': run_tests()
