"""Redraw the Markdown draft diagrams; no source screenshots are published."""
from pathlib import Path
import os
import math
ROOT = Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR'] = str(ROOT / 'work' / 'mpl-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

OUT = ROOT / 'assets' / 'diagrams'
OUT.mkdir(parents=True, exist_ok=True)
TIKZ = []
plt.rcParams.update({'font.family': 'DejaVu Serif', 'mathtext.fontset': 'dejavuserif',
                     'svg.fonttype': 'path'})
INK = '#34373c'
BLUE = '#355c86'

def add(p,q): return tuple(a+b for a,b in zip(p,q))
def sub(p,q): return tuple(a-b for a,b in zip(p,q))
def mul(t,p): return tuple(t*a for a in p)
def dot(p,q): return sum(a*b for a,b in zip(p,q))
def unit(p): return mul(1/math.sqrt(dot(p,p)),p)
def foot(p,a,b):
    v=sub(b,a)
    return add(a,mul(dot(sub(p,a),v)/dot(v,v),v))
def intersect(a,b,c,d):
    v=sub(b,a); w=sub(d,c); z=sub(c,a)
    det=lambda p,q:p[0]*q[1]-p[1]*q[0]
    return add(a,mul(det(z,w)/det(v,w),v))

class Figure:
    def __init__(self, pts, base, offsets=None):
        self.pts=pts.copy(); self.offsets=offsets or {}
        self.fig,self.ax=plt.subplots(figsize=(6.2,4.8))
        self.ax.set_aspect('equal');self.ax.axis('off')
        self.tex=[r'\begin{tikzpicture}[scale=.8,line width=.7pt,every node/.style={font=\small,inner sep=2pt}]']
        for k,p in pts.items():
            self.tex.append(f'\\coordinate ({k}) at ({p[0]:.8f},{p[1]:.8f});')
        for a,b in base:self.line(a,b)
    def line(self,a,b,aux=False):
        p,q=self.pts[a],self.pts[b]
        self.ax.plot([p[0],q[0]],[p[1],q[1]],color=BLUE if aux else INK,
                     lw=1.7,linestyle=(0,(4,3)) if aux else '-',zorder=2)
        self.tex.append(f'\\draw[{"esblue,dashed" if aux else "inkiron"}] ({a}) -- ({b});')
    def highlight(self,keys,color):
        points=[self.pts[k] for k in keys]
        self.ax.add_patch(Polygon(points,closed=True,facecolor=color,alpha=.18,
                                  edgecolor='none',zorder=1))
        ring=points+[points[0]]
        self.ax.plot([p[0] for p in ring],[p[1] for p in ring],color=color,
                     lw=2,zorder=3)
        dye='esblue' if color==BLUE else 'esorange'
        path=' -- '.join(f'({k})' for k in keys)+' -- cycle'
        self.tex.append(f'\\filldraw[fill={dye}!18,draw={dye},line width=1pt] {path};')
    def right(self,a,o,b,s=.17):
        p=self.pts[o];u=unit(sub(self.pts[a],p));v=unit(sub(self.pts[b],p))
        assert abs(dot(u,v))<1e-8, (a,o,b)
        qs=[add(p,mul(s,u)),add(p,mul(s,add(u,v))),add(p,mul(s,v))]
        self.ax.plot([q[0] for q in qs],[q[1] for q in qs],color='#718080',lw=1)
        self.tex.append('\\draw[selvage] '+' -- '.join(f'({q[0]:.8f},{q[1]:.8f})' for q in qs)+';')
    def tick(self,a,b,n=1,at=.5):
        p,q=self.pts[a],self.pts[b];u=unit(sub(q,p));v=(-u[1],u[0]);mid=add(p,mul(at,sub(q,p)))
        for j in range(n):
            m=add(mid,mul((j-(n-1)/2)*.11,u));w=mul(.12,v)
            x,y=sub(m,w),add(m,w)
            self.ax.plot([x[0],y[0]],[x[1],y[1]],color=INK,lw=1.2)
            frac=at+(j-(n-1)/2)*.11/math.dist(p,q)
            self.tex.append(f'\\draw[inkiron] ($({a})!{frac:.8f}!({b})!3pt!90:({b})$) -- ($({a})!{frac:.8f}!({b})!3pt!-90:({b})$);')
    def angle(self,a,o,b,label,r=.55):
        p=self.pts[o];u=sub(self.pts[a],p);v=sub(self.pts[b],p)
        lo=math.atan2(u[1],u[0]); hi=math.atan2(v[1],v[0]);delta=(hi-lo+math.pi)%(2*math.pi)-math.pi
        ts=[lo+delta*i/40 for i in range(41)]
        self.ax.plot([p[0]+r*math.cos(t) for t in ts],[p[1]+r*math.sin(t) for t in ts],color=BLUE,lw=1)
        t=lo+delta/2
        self.ax.text(p[0]+1.45*r*math.cos(t),p[1]+1.45*r*math.sin(t),label,
                     ha='center',va='center',fontsize=12,color=BLUE)
        self.tex.append('\\draw[esblue] '+' -- '.join(f'({p[0]+r*math.cos(t):.8f},{p[1]+r*math.sin(t):.8f})' for t in ts)+';')
    def save(self,name):
        for k,p in self.pts.items():
            off=self.offsets.get(k,(0,.25))
            self.ax.plot(*p,'o',color=INK,ms=3,zorder=4)
            self.ax.text(p[0]+off[0],p[1]+off[1],'$'+k+'$',ha='center',va='center',fontsize=15)
            self.tex.append(f'\\fill[inkiron] ({k}) circle (1pt);')
            self.tex.append(f'\\node at ({p[0]+off[0]:.8f},{p[1]+off[1]:.8f}) {{${k}$}};')
        self.ax.margins(.13)
        self.fig.savefig(OUT/(name+'.png'),dpi=190,bbox_inches='tight',facecolor='white')
        self.fig.savefig(OUT/(name+'.svg'),bbox_inches='tight',facecolor='white')
        plt.close(self.fig)
        macro='esdi'+''.join(part.title() for part in name.split('-'))
        TIKZ.append('\\newcommand{\\'+macro+'}{%\n'+'\n'.join(self.tex)+ '\n\\end{tikzpicture}}\n')

A=(4.,4.);B=(0.,0.);C=(8.,0.);D=(7.2,2.4)
base=[('A','B'),('B','C'),('C','D'),('D','A'),('A','C'),('B','D')]
pts={'A':A,'B':B,'C':C,'D':D}
offsets={'A':(-.15,.28),'B':(-.25,-.25),'C':(.25,-.25),'D':(.35,.03)}
O=intersect(A,C,B,D)
f=Figure({**pts,'O':O},base,{**offsets,'O':(-.3,-.25)})
f.highlight(['A','B','O'],BLUE)
f.highlight(['D','C','O'],'#b76543')
f.right('B','A','O');f.right('O','D','C')
f.save('model')
f=Figure({**pts,'X':add(D,mul(1.4,sub(D,C)))},base,offsets)
f.line('D','X',True);f.angle('B','D','A','');f.angle('A','D','X','')
# The midpoint of AC is its crossing with BD; keep the length mark clear of it.
f.right('B','A','C');f.right('B','D','C');f.tick('A','B');f.tick('A','C',at=.3);f.save('exterior')
f=Figure(pts,base,offsets);f.right('B','A','C');f.right('B','D','C');f.tick('A','B');f.tick('A','C',at=.3);f.save('shared-hypotenuse')
M=foot(A,B,D);N=foot(A,C,D)
f=Figure({**pts,'M':M,'N':N},base,{**offsets,'M':(0,-.35),'N':(.25,.25)})
for a,b in [('A','M'),('A','N'),('D','N')]:f.line(a,b,True)
f.right('A','M','B');f.right('A','N','C');f.save('double-perpendicular')
E=add(D,mul(math.dist(B,D)/math.dist(C,D),sub(D,C)))
f=Figure({**pts,'E':E},base,offsets)
f.line('D','E',True);f.line('A','E',True);f.tick('D','E',2);f.tick('D','B',2);f.save('extend-cd')
F=add(D,mul(math.dist(C,D)/math.dist(B,D),sub(D,B)))
f=Figure({**pts,'F':F},base,offsets)
f.line('D','F',True);f.line('A','F',True);f.tick('D','F',2);f.tick('D','C',2);f.save('extend-bd')
P=intersect(A,add(A,(-sub(D,A)[1],sub(D,A)[0])),B,D)
f=Figure({**pts,'P':P},base,{**offsets,'P':(0,-.35)})
f.line('A','P',True);f.right('P','A','D');f.tick('A','P',2);f.tick('A','D',2);f.save('hand-lower')
Q=intersect(A,add(A,(-sub(D,A)[1],sub(D,A)[0])),C,D)
f=Figure({**pts,'Q':Q},base,offsets)
f.line('D','Q',True);f.line('A','Q',True);f.right('Q','A','D');f.tick('A','Q',2);f.tick('A','D',2);f.save('hand-upper')
M=foot(B,A,D);N=foot(C,A,D)
f=Figure({**pts,'M':M,'N':N},base,{**offsets,'M':(-.2,.25),'N':(.3,.05)})
for a,b in [('B','M'),('M','A'),('C','N'),('D','N')]:f.line(a,b,True)
f.right('B','M','A');f.right('C','N','A');f.save('k-perpendicular')

# Photographed example; each solution uses its own F.
t=math.sqrt(2)-1
A=(4.,4.);B=(0.,0.);C=(8.,0.);D=(4+4*t,4-4*t);E=foot(C,B,D)
pts={'A':A,'B':B,'C':C,'D':D,'E':E}
base=[('A','B'),('B','C'),('A','C'),('B','E'),('C','E')]
offsets={'A':(-.1,.28),'B':(-.25,-.25),'C':(.25,-.25),'D':(.35,.35),'E':(.3,.18)}
def example(extra=None,off=None):
    f=Figure({**pts,**(extra or {})},base,{**offsets,**(off or {})})
    f.right('B','A','C');f.right('B','E','C');f.tick('A','B');f.tick('A','C')
    f.angle('A','B','D','',r=1.1);f.angle('D','B','C','',r=1.1)
    return f
f=example();f.save('example')
F=intersect(B,A,C,E)
f=example({'F':F});f.line('A','F',True);f.line('E','F',True);f.save('example-extend')
F=intersect(D,add(D,sub(A,B)),B,C);G=foot(F,B,D)
f=example({'F':F,'G':G},{'F':(0,-.35),'G':(-.35,.1)})
f.line('D','F',True);f.line('F','G',True);f.right('F','G','B');f.tick('B','F',2);f.tick('D','F',2);f.save('example-parallel')
F=intersect(A,add(A,(-sub(E,A)[1],sub(E,A)[0])),B,D)
f=example({'F':F},{'F':(0,-.4)})
f.line('A','F',True);f.line('A','E',True);f.right('F','A','E',s=.32);f.tick('A','F',2);f.tick('A','E',2);f.save('example-hand')
F=sub(mul(2,E),C)
f=example({'F':F});f.line('E','F',True);f.line('B','F',True);f.tick('C','E',2);f.tick('E','F',2);f.save('example-reflect')
(ROOT/'latex').mkdir(exist_ok=True)
(ROOT/'latex/diagrams.tex').write_text('% Generated from the same coordinates as PNG/SVG.\n'+
    '\n'.join(TIKZ),encoding='utf-8')
print('PASS: generated 14 matching PNG/SVG/TikZ diagrams; all drawn right angles verified.')
