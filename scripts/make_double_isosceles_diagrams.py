"""Generate matching TikZ, SVG and PNG diagrams for the double-isosceles chapter."""
from pathlib import Path
import math
import os
os.environ['MPLCONFIGDIR']=str(Path(__file__).resolve().parent.parent/'tmp'/'double-isosceles-mpl-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Arc

ROOT=Path(__file__).resolve().parent.parent
CH=ROOT/'chapters/03-double-isosceles'
OUT=CH/'assets/diagrams'
OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Serif','mathtext.fontset':'dejavuserif',
                     'svg.fonttype':'path'})
INK='#34373c'; INDIGO='#355c86'; RED='#95473f'; GRAY='#718080'
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(s,a):return tuple(s*x for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def unit(a):return mul(1/math.sqrt(dot(a,a)),a)
def project(a,v):return mul(dot(a,v)/dot(v,v),v)
B=(0,0); C=(-6,2); Cp=(-2,-6); D=(3,1); Dp=(-1,3)
E=mul(.5,add(C,Dp)); G=mul(2,E); base=sub(D,Cp)
F=add(Cp,mul(-dot(Cp,base)/dot(base,base),base))
M1=project(Dp,C); N1=project(D,Cp)
M3=project(C,E); N3=project(Dp,E)
labels={'B':('B',(-.46,-.45)),'C':('C',(-.45,.10)),
        'Cp':("C'",(-.20,-.42)),'D':('D',(.36,.12)),
        'Dp':("D'",(.32,.26)), 'E':('E',(.02,.35)),
        'G':('G',(-.2,.35)),'F':('F',(.30,-.23)),
        'H':('H',(.30,-.23)),'M':('M',(-.28,.36)),
        'N':('N',(.38,.03))}
tikz=[]

def draw(name,macro,kind):
    fig,ax=plt.subplots(figsize=(5.7,6.4)); ax.set_aspect('equal');ax.axis('off')
    pts={'B':B,'C':C,'Cp':Cp,'D':D,'Dp':Dp}
    scale={'review':1.2,'model':.47,'area':.47,'midpoint':.45,'converse':.52}[kind]
    tex=[f'\\newcommand{{\\{macro}}}{{%',
         f'\\begin{{tikzpicture}}[scale={scale},line width=.7pt,every node/.style={{font=\\small,inner sep=2pt}}]']
    def coord(k,p):
        pts[k]=p;tex.append(f'\\coordinate ({k}) at ({p[0]:.8f},{p[1]:.8f});')
    def line(a,b,aux=False):
        p,q=pts[a],pts[b];color=INDIGO if aux else INK
        ax.plot([p[0],q[0]],[p[1],q[1]],color=color,lw=1.6 if aux else 1.7,
                linestyle=(0,(4,3)) if aux else '-',zorder=3)
        tex.append(f'\\draw[{"indigo,dashed" if aux else "inkiron"}] ({a}) -- ({b});')
    def fill(keys,color,texcolor):
        ax.add_patch(Polygon([pts[k] for k in keys],facecolor=color,alpha=.12,edgecolor='none'))
        tex.append(f'\\fill[{texcolor}!10] '+' -- '.join(f'({k})' for k in keys)+' -- cycle;')
    def right(a,o,b):
        p=pts[o];u=unit(sub(pts[a],p));v=unit(sub(pts[b],p));s=.24
        corners=[add(p,mul(s,u)),add(p,mul(s,add(u,v))),add(p,mul(s,v))]
        ax.plot([q[0] for q in corners],[q[1] for q in corners],color=GRAY,lw=1,zorder=4)
        tex.append(f'\\pic[draw=selvage,angle radius=2.2mm] {{right angle={a}--{o}--{b}}};')
    def tick(a,b,n=1,color=INK,texcolor='inkiron'):
        p,q=pts[a],pts[b];u=unit(sub(q,p));v=(-u[1],u[0]);mid=mul(.5,add(p,q))
        for i in range(n):
            t=(i-(n-1)/2)*.11;m=add(mid,mul(t,u));w=mul(.15,v)
            x,y=sub(m,w),add(m,w);ax.plot([x[0],y[0]],[x[1],y[1]],color=color,lw=1.2,zorder=5)
            frac=.5+t/math.sqrt(dot(sub(q,p),sub(q,p)))
            tex.append(f'\\draw[{texcolor}] ($({a})!{frac:.8f}!({b})!3pt!90:({b})$) -- ($({a})!{frac:.8f}!({b})!3pt!-90:({b})$);')
    def points_and_labels(overrides=None):
        for k,p in pts.items():
            label,offset=overrides[k] if overrides and k in overrides else labels[k]
            pos=add(p,offset)
            ax.plot(*p,'o',color=INK,ms=3.3,zorder=6)
            ax.text(*pos,'$'+label+'$',fontsize=15,ha='center',va='center',color=INK,zorder=7)
            tex.append(f'\\fill[inkiron] ({k}) circle (1.05pt);')
            tex.append(f'\\node at ({pos[0]:.8f},{pos[1]:.8f}) {{${label}$}};')
    if kind=='review':
        pts={};review={'A':(-1,0),'B':(0,0),'C':(2,0),'D':(-1,2),'E':(2,1)}
        for k,p in review.items():coord(k,p)
        for a,b in [('A','C'),('A','D'),('B','D'),('B','E'),('C','E')]:line(a,b)
        right('D','A','B');right('D','B','E');right('B','C','E')
        tick('B','D');tick('B','E')
        points_and_labels({'A':('A',(-.15,-.27)),'B':('B',(0,-.30)),
                           'C':('C',(.10,-.27)),'D':('D',(-.10,.26)),'E':('E',(.24,.05))})
    else:
        for k,p in list(pts.items()):coord(k,p)
        fill(['C','B','Dp'],GRAY,'selvage');fill(['Cp','B','D'],RED,'madder')
        for a,b in [('B','C'),('B','Cp'),('B','D'),('B','Dp'),('C','Dp'),('Cp','D')]:line(a,b)
        right('C','B','Cp');right('D','B','Dp')
        tick('B','C');tick('B','Cp');tick('B','D',2);tick('B','Dp',2)
        if kind=='area':
            coord('M',M1);coord('N',N1)
            line('Dp','M',True);line('D','N',True);line('B','N',True)
            right('B','M','Dp');right('B','N','D')
            points_and_labels({'M':('M',(-.33,-.22)),'N':('N',(.04,.36))})
        elif kind=='midpoint':
            coord('E',E);coord('G',G);coord('H',F)
            line('G','H',True);line('C','G',True)
            tick('C','E',3,INDIGO,'indigo');tick('E','Dp',3,INDIGO,'indigo')
            tick('B','E',2,RED,'madder');tick('E','G',2,RED,'madder')
            points_and_labels({'E':('E',(.05,.43))})
        elif kind=='converse':
            coord('E',E);coord('F',F);coord('M',M3);coord('N',N3)
            line('M','F',True);line('C','M',True);line('Dp','N',True)
            right('C','M','B');right('Dp','N','B');right('B','F','D')
            points_and_labels({'E':('E',(.04,.40)),'M':('M',(-.10,.40)),
                               'N':('N',(-.12,-.36))})
        else:points_and_labels()
    tex.append('\\end{tikzpicture}}\n')
    tikz.extend(tex)
    ax.margins(.12)
    fig.savefig(OUT/f'{name}.png',dpi=210,bbox_inches='tight',facecolor='white')
    fig.savefig(OUT/f'{name}.svg',bbox_inches='tight',facecolor='white')
    svg=OUT/f'{name}.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
    plt.close(fig)

for args in [('review','diReview','review'),('model','diModel','model'),
             ('area','diArea','area'),('midpoint','diMidpoint','midpoint'),
             ('converse','diConverse','converse')]:draw(*args)
(CH/'latex').mkdir(exist_ok=True)
(CH/'latex/diagrams.tex').write_text('% Same coordinates as the SVG/PNG diagrams.\n'+'\n'.join(tikz),encoding='utf-8')
print('Generated five matching PNG/SVG/TikZ diagrams.')
