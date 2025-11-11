def solution(A,B):
    n=len(A); m=len(A[0]); p=len(B[0])
    C=[[0]*p for _ in range(n)]
    for i in range(n):
        for k in range(m):
            aik=A[i][k]
            for j in range(p):
                C[i][j]+=aik*B[k][j]
    return C
def run_tests():
    A=[[1,2],[3,4]]; B=[[5,6],[7,8]]
    assert solution(A,B)==[[19,22],[43,50]]
if __name__=='__main__': run_tests()
