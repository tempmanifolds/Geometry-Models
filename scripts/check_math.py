"""Verify exact numerical answers and stated model identities with fractions."""
from fractions import Fraction as F
from math import sqrt

def angle45(u,v):
    dot=u[0]*v[0]+u[1]*v[1]
    cross=u[0]*v[1]-u[1]*v[0]
    assert dot>0 and dot==abs(cross), (u,v,dot,cross)

# 题1与题2/3
assert F(5,2)**2==2**2+F(3,2)**2
angle45((1,-3),(3,F(-3,2)))
x=F(9,2)
assert 6**2+(9-x)**2==(3+x)**2
angle45((3,9),(9,x))

# 题4 垂直与等长
assert (-1)*3+(-3)*(-1)==0
assert 1**2+3**2==3**2+(-1)**2

# 题5 底边高与三种构造
h,p,q=F(6),F(3),F(2)
assert (p+q)**2==(h-p)**2+(h-q)**2
angle45((-p,-h),(q,-h))

# 题6 截形结果，恢复到原矩形
x=F(2)
assert (3+x)**2==3**2+(6-x)**2
assert 2*x==4
angle45((3,-6),(12,-4))

# 题7 原图的交点、夹角及转化后的通式
ce=F(30,11); fx=F(120,73); fy=F(174,73)
assert fy==6-6*fx/ce==3-F(3,8)*fx
assert 0<fx<ce and 0<fy<3
angle45((8-fx,-fy),(ce-fx,-fy))
assert ce==6*(6-F(9,4))/(6+F(9,4))

# 题8 x=5, AB=8, BC=9
x=F(5)
assert 2*x*x==1**2+7**2
angle45((4,-8),(9,-3))

# 题9 内外构型
angle45((3,1),(F(3,2),3))
assert (3-F(3,2))**2+(3-1)**2==(1+F(3,2))**2
angle45((3,6),(-1,3))
assert (3+1)**2+(6-3)**2==(6-1)**2

# 题10 两个根都满足原始角度；旋转图中的3-4-5三角形
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
        angle45((m,-s),(s,-n))  # 原稿图B/C转化关系

# 底边高通式与逆推
for k in range(1,32):
    h=F(6);p=h*F(k,32);q=h*(h-p)/(h+p)
    assert 0<p<h and 0<q<h
    assert (p+q)**2==(h-p)**2+(h-q)**2
    angle45((-p,-h),(q,-h))
print('PASS: all 10 problems, both roots of problem 10, and model identities')
