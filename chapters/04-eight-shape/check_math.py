"""Author-side checks for the Markdown draft. Run from the project root."""
from fractions import Fraction as Q
from itertools import combinations
from sympy import Point, Line, sqrt, simplify, pi

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(k,a):return tuple(k*x for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def dist2(a,b):return dot(sub(a,b),sub(a,b))
def foot(p,a,b):
    v=sub(b,a)
    return add(a,mul(dot(sub(p,a),v)/dot(v,v),v))
def intersect(a,b,c,d):
    v=sub(b,a);w=sub(d,c)
    return add(a,mul(det(sub(c,a),w)/det(v,w),v))
def congruent(t,u):
    for i,j in combinations(range(3),2):assert dist2(t[i],t[j])==dist2(u[i],u[j])

A=(Q(1),Q(1));B=(Q(0),Q(0));C=(Q(2),Q(0));count=0
for m in range(2,20):
    for n in range(1,m):
        c=Q(m*m-n*n,m*m+n*n);s=Q(2*m*n,m*m+n*n)
        if c<=s:continue
        D=(2*c*c,2*c*s)
        assert dot(sub(B,A),sub(C,A))==dot(sub(B,D),sub(C,D))==0
        M=foot(A,B,D);N=foot(A,C,D)
        assert 0<dot(M,D)<dot(D,D)
        congruent((A,B,M),(A,C,N));congruent((A,D,M),(A,D,N))
        E=add(D,mul(c/s,sub(D,C)));F=add(D,mul(s/c,D))
        congruent((A,B,D),(A,E,D));congruent((A,D,C),(A,D,F))
        v=sub(D,A);perp=(-v[1],v[0])
        P=intersect(A,add(A,perp),B,D);U=intersect(A,add(A,perp),C,D)
        congruent((A,B,P),(A,C,D));congruent((A,B,D),(A,C,U))
        assert dist2(A,P)==dist2(A,D)==dist2(A,U)
        assert dot(sub(P,A),sub(D,A))==dot(sub(U,A),sub(D,A))==0
        K=foot(B,A,D);L=foot(C,A,D)
        congruent((A,B,K),(C,A,L))
        assert dist2(B,K)==dist2(D,K) and dist2(C,L)==dist2(D,L)
        assert dist2(A,K)==dist2(D,L) and dist2(A,L)==dist2(D,K)
        count+=1

# Exact irrational coordinates for all four photographed solutions.
def equal(x,y):assert simplify(x-y)==0,(x,y)
def sq(p,q):return simplify(p.distance(q)**2)
def s_congruent(t,u):
    for i,j in combinations(range(3),2):equal(sq(t[i],t[j]),sq(u[i],u[j]))
t=sqrt(2)-1;A=Point(0,0);B=Point(-1,-1);C=Point(1,-1);D=Point(t,-t)
E=Line(B,D).projection(C)
equal(sq(B,D),4*sq(C,E))
F=Line(B,A).intersection(Line(C,E))[0]
s_congruent((A,B,D),(A,C,F));equal(sq(C,E),sq(F,E))
F=Line(D,D+(A-B)).intersection(Line(B,C))[0];G=Line(B,D).projection(F)
equal(sq(B,F),sq(D,F));equal(sq(D,F),sq(D,C));equal(sq(B,G),sq(D,G))
s_congruent((D,F,G),(C,D,E));equal(sq(D,G),sq(C,E))
F=Line(B,D).intersection(Line(A,A+(A-E).rotate(pi/2)))[0]
s_congruent((A,B,F),(A,C,E));equal(sq(A,F),sq(A,E));equal(sq(B,F),sq(F,D))
equal(F.x,(B.x+D.x)/2);equal(F.y,(B.y+D.y)/2)
F=2*E-C
s_congruent((B,E,C),(B,E,F));equal(Line(B,A).distance(F),0)
s_congruent((A,B,D),(A,C,F))

# Opposite sides of BC give an internal bisector, so orientation is essential.
A=Point(0,1);B=Point(-1,0);C=Point(1,0);D=Point(0,-1);X=2*D-C
equal(sq(A,B),sq(A,C))
equal((A-B).dot(A-C),0);equal((D-B).dot(D-C),0)
assert simplify((A-D).dot(B-D))>0 and simplify((A-D).dot(X-D))<0
# Same-side right angles without equal legs do not imply the external bisector.
A=Point(Q(2,5),Q(4,5));B=Point(0,0);C=Point(2,0);D=Point(Q(8,5),Q(4,5))
equal((A-B).dot(A-C),0);equal((D-B).dot(D-C),0)
assert sq(A,B)!=sq(A,C)
assert simplify(Line(B,D).distance(A)**2-Line(C,D).distance(A)**2)!=0
print(f'PASS: {count} rational model configurations; all congruence correspondences, '
      'two K-type constructions, four exact example solutions, and orientation counterexample.')
