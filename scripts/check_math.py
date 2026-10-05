"""Verify exact numerical answers and stated model identities with fractions."""
from fractions import Fraction as F
from math import sqrt

def angle45(u,v):
    dot=u[0]*v[0]+u[1]*v[1]
    cross=u[0]*v[1]-u[1]*v[0]
    assert dot>0 and dot==abs(cross), (u,v,dot,cross)

# 图A与题1/2
assert F(5,2)**2==2**2+F(3,2)**2
angle45((1,-3),(3,F(-3,2)))
x=F(9,2)
assert 6**2+(9-x)**2==(3+x)**2
angle45((3,9),(9,x))

# 题3 垂直与等长
assert (-1)*3+(-3)*(-1)==0
assert 1**2+3**2==3**2+(-1)**2

# 题4 底边高与三种构造
h,p,q=F(6),F(3),F(2)
assert (p+q)**2==(h-p)**2+(h-q)**2
angle45((-p,-h),(q,-h))

# 例题4的实际题图：核对旋转点、翻折点和两条延长射线的方向。
def sub(a,b):
    return (a[0]-b[0],a[1]-b[1])

def dot(a,b):
    return a[0]*b[0]+a[1]*b[1]

def norm2(a):
    return dot(a,a)

def reflection(point, origin, axis_end):
    v=sub(point,origin); axis=sub(axis_end,origin)
    factor=2*dot(v,axis)/norm2(axis)
    return (origin[0]+factor*axis[0]-v[0],
            origin[1]+factor*axis[1]-v[1])

a=(F(0),h); b=(-p,F(0)); c=(q,F(0)); d=(F(0),F(0))
e1=reflection(d,a,b); f1=reflection(d,a,c)
assert e1 == (F(-24,5),F(12,5))
assert f1 == (F(18,5),F(6,5))
fold_p=(F(-6,5),F(-12,5))
assert norm2(sub(e1,a)) == norm2(sub(f1,a)) == h*h
assert dot(sub(e1,a),sub(f1,a)) == 0
assert sub(fold_p,e1) == tuple(2*v for v in sub(b,e1))  # E1、B、P
assert sub(fold_p,f1) == tuple(3*v for v in sub(c,f1))  # F1、C、P
assert norm2(sub(fold_p,b)) == 3**2
assert norm2(sub(fold_p,c)) == 4**2
square_g=(-h,h-q); extension_g=(h,h-p)
assert norm2(sub(square_g,a)) == norm2(sub(c,a))
assert norm2(sub(square_g,b)) == norm2(sub(c,b))
assert norm2(sub(extension_g,a)) == norm2(sub(b,a))
assert norm2(sub(extension_g,c)) == norm2(sub(b,c))

# 题5 截形结果，恢复到原矩形
x=F(2)
assert (3+x)**2==3**2+(6-x)**2
assert 2*x==4
angle45((3,-6),(12,-4))

# 题6 原图的交点、夹角及转化后的通式
ce=F(30,11); fx=F(120,73); fy=F(174,73)
assert fy==6-6*fx/ce==3-F(3,8)*fx
assert 0<fx<ce and 0<fy<3
angle45((8-fx,-fy),(ce-fx,-fy))
assert ce==6*(6-F(9,4))/(6+F(9,4))

# 题7 x=5, AB=8, BC=9
x=F(5)
assert 2*x*x==1**2+7**2
angle45((4,-8),(9,-3))

# 题8 内外构型
angle45((3,1),(F(3,2),3))
assert (3-F(3,2))**2+(3-1)**2==(1+F(3,2))**2
angle45((3,6),(-1,3))
assert (3+1)**2+(6-3)**2==(6-1)**2

# 题9 两个根都满足原始角度；旋转图中的3-4-5三角形
for t in [F(3),F(6)]:
    angle45((4-t,-t),(9-t,-t))
    assert (9-2*t)**2+4**2==5**2

# 拓展与识别图：精确检查31个内部位置的乘积、定周长与定高。
for s in [F(3),F(9),F(13,2)]:
    for k in range(1,32):
        m=s*F(k,32); n=s*(s-m)/(s+m); L=m+n
        assert 0<m<s and 0<n<s
        assert (s-m)**2+(s-n)**2==L**2
        assert (s+m)*(s+n)==2*s*s
        assert (s-m)+(s-n)+L==2*s
        assert (s*s-m*n)/L==s  # 三角形的2倍面积/底边
        assert 2*(sqrt(2)-1)*float(s)-1e-12<=float(L)<float(s)
        angle45((m,s),(s,n))
        # 图 A：旋转后 G=(s,s+m)，EF=FG=m+n。
        assert (s-m)**2+(s-n)**2 == (m+n)**2
        angle45((m,-s),(s,-n))
        assert s-n == 2*s*m/(s+m)  # CF 的显式公式

        # 图 B：F=(0,n)，AG=(s,-n) 与 FC 平行，DG=BF=n。
        bx = m*s*(s-n)/(s*s-m*n)
        by = s-s*bx/m
        assert 0<bx<m and 0<by<n
        assert by == n-n*bx/s  # P 同时位于 AE、FC 上
        angle45((m-bx,-by),(s-bx,-by))
        assert (s-m)**2+(s-n)**2 == (m+n)**2  # EG=BE+BF

        # 图 C：F=(n,s)，AG=(s,-n) 与 BF=(n,s) 垂直。
        cx = m*n/(m+n)
        cy = s*m/(m+n)
        assert cy == s-s*cx/m == s*cx/n
        assert 0<cx<m and 0<cy<s
        assert dot((s,-n),(n,s)) == 0
        angle45((-cx,s-cy),(n-cx,s-cy))  # ∠APF=45°

        # 图 D：在每个半角构型上平移两条原线，保留边内点及交点。
        ae=(s-m)/3; am=(s-n)/4
        bf=m+ae; dn=n+am
        assert 0<ae<bf<s and 0<am<dn<s
        t=(s*am+n*ae)/(s*s-m*n)
        u=(s*ae+m*am)/(s*s-m*n)
        assert 0<t<1 and 0<u<1  # P 在 EF、MN 内部
        assert ae+m*t == s*u
        assert s-s*t == s-am-n*u
        assert bf-ae == m and dn-am == n
        angle45((m,-s),(s,-n))  # ∠FPN 与 ∠TAU
        assert (s-m)**2+(s-n)**2 == ((bf-ae)+(dn-am))**2

# 图 D 绘图所用的精确交点及两条平移线。
de=(F(13,20),F(3)); df=(F(33,20),F(0))
dm=(F(0),F(49,20)); dn=(F(3),F(19,20)); dp=(F(1),F(39,20))
assert sub(dp,de) == tuple(F(7,20)*v for v in sub(df,de))
assert sub(dp,dm) == tuple(F(1,3)*v for v in sub(dn,dm))
angle45(sub(df,dp),sub(dn,dp))
assert df[0]-de[0] == F(1)
assert (3-dn[1])-(3-dm[1]) == F(3,2)

# 底边高通式与逆推
for k in range(1,32):
    h=F(6);p=h*F(k,32);q=h*(h-p)/(h+p)
    assert 0<p<h and 0<q<h
    assert (p+q)**2==(h-p)**2+(h-q)**2
    angle45((-p,-h),(q,-h))
print('PASS: all 9 numbered items, four configurations (93 exact cases), both roots of problem 9, and model identities')
