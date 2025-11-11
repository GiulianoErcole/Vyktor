def relu(x): return x if x>0 else 0
def solution(x, w, b):
    s = sum(xi*wi for xi,wi in zip(x,w)) + b
    return relu(s)
def run_tests():
    out=solution([1.0, -2.0, 0.5],[0.5, 0.3, -0.2],0.1)
    assert isinstance(out,(int,float))
if __name__=='__main__': run_tests()
