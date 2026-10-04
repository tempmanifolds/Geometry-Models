"""Exact coordinate checks of the chapter's congruences and companion length."""
from fractions import Fraction as Q
from itertools import product

def add(u,v):return tuple(a+b for a,b in zip(u,v))
def sub(u,v):return tuple(a-b for a,b in zip(u,v))
def mul(k,u):return tuple(k*a for a in u)
def dot(u,v):return sum(a*b for a,b in zip(u,v))
def det(u,v):return u[0]*v[1]-u[1]*v[0]
def norm2(u):return dot(u,u)
def dist2(u,v):return norm2(sub(u,v))
def rot(u):return (-u[1],u[0])
def project(u,v):return mul(Q(dot(u,v),norm2(v)),v)
def congruent(t,u):
    for i,j in ((0,1),(1,2),(2,0)):
        assert dist2(t[i],t[j])==dist2(u[i],u[j]),(t,u,i,j)

B=(Q(0),Q(0))
def check(C,D):
    Cp=rot(C);Dp=rot(D);E=mul(Q(1,2),add(C,Dp));G=mul(2,E)
    v=sub(D,Cp);F=add(Cp,project(mul(-1,Cp),v))
    M1=project(Dp,C);N1=project(D,Cp)
    assert dot(sub(Dp,M1),C)==dot(sub(D,N1),Cp)==0
    congruent((B,M1,Dp),(B,N1,D))
    assert abs(det(C,Dp))==abs(det(Cp,D))
    congruent((C,E,G),(Dp,E,B))
    assert det(sub(G,C),Dp)==0
    congruent((G,C,B),(D,B,Cp))
    assert dot(E,v)==0 and norm2(mul(2,E))==norm2(v)
    # Derive E a second way: intersect the perpendicular line BF with CD'.
    w=sub(Dp,C);t=-Q(dot(C,v),dot(w,v));reverse_E=add(C,mul(t,w))
    assert reverse_E==E and dist2(C,E)==dist2(Dp,E)
    M3=project(C,F);N3=project(Dp,F)
    congruent((B,C,M3),(Cp,B,F))
    congruent((B,Dp,N3),(D,B,F))
    assert dist2(C,M3)==norm2(F)==dist2(Dp,N3)
    congruent((C,M3,E),(Dp,N3,E))
    # E is the midpoint of both the two endpoints and their projections.
    assert add(M3,N3)==mul(2,E)
    # Area reconstruction uses the determinant, without irrational rounding.
    assert det(C,Dp)**2==4*norm2(E)*norm2(F)==det(Cp,D)**2
    return E,G,F,M3,N3

count=degenerate=0
for a,b,c,d in product(range(1,6),repeat=4):
    C=(-Q(a),Q(b));D=(Q(c),Q(d))
    if dot(C,D)>=0:continue # the same nondegenerate angular order as the chapter
    E,G,F,M,N=check(C,D);count+=1
    degenerate+=M==E==N

example=check((-Q(6),Q(2)),(Q(3),Q(1)))
assert example==((Q(-7,2),Q(5,2)),(Q(-7),Q(5)),
                 (Q(56,37),Q(-40,37)),(Q(-182,37),Q(130,37)),
                 (Q(-77,37),Q(55,37)))
assert norm2(example[2])==Q(128,37)
assert dist2((-Q(6),Q(2)),example[0])==Q(13,2)
# A mirrored second isosceles triangle satisfies lengths and right angles,
# but must not be accepted for the midpoint/perpendicular conclusions.
C=(-Q(6),Q(2));D=(Q(3),Q(1));Cp=mul(-1,rot(C));Dp=rot(D)
assert dot(mul(Q(1,2),add(C,Dp)),sub(D,Cp))!=0
print(f'PASS: {count} exact configurations; {degenerate} coincident-foot cases; '
      'all stated lengths, congruences, areas and orientation counterexample.')
