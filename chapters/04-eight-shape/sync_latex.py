"""Synchronize this chapter's reviewed Markdown with modular LaTeX sections."""
from pathlib import Path
import re

CH=Path(__file__).resolve().parent
SECTIONS=CH/'latex/sections'

def math_tex(s):
    for a,b in [('Rt△',r'\mathrm{Rt}\triangle '),('△',r'\triangle '),
                ('∠',r'\angle '),('⊥',r'\perp '),('∥',r'\parallel '),
                ('≅',r'\cong '),('＝','='),('＋','+'),('－','-'),('°',r'^\circ')]:
        s=s.replace(a,b)
    if s in ['ASA','AAS','SAS','HL']:s=r'\mathrm{'+s+'}'
    return s

TOKEN=r'(?:Rt△[A-Z]+|△[A-Z]+|∠[A-Z]+|[A-Z]+|\d+(?:\.\d+)?(?:°)?)'
RUN=re.compile(TOKEN+r'(?:[＝=＋+－\-⊥∥≅]'+TOKEN+r')*')

def inline(s):
    # Preserve explicit math, including condition labels in \text{}.
    pieces=re.split(r'(\$[^$]*\$)',s)
    for i in range(0,len(pieces),2):
        t=pieces[i]
        t=RUN.sub(lambda m:'$'+math_tex(m.group())+'$',t)
        t=re.sub(r'\*\*([^*]+)\*\*',lambda m:r'\textbf{'+m.group(1)+'}',t)
        pieces[i]=t
    result=''.join(pieces)
    return re.sub('[①②③④]',lambda m:r'\escond{'+str('①②③④'.index(m.group())+1)+'}',result)

def heading(s):
    plain=re.sub(r'\\text\{([^}]+)\}',r'\1',s).replace(r'\Rightarrow','⇒').replace('$','')
    return r'\texorpdfstring{'+inline(s)+'}{'+plain+'}'

def convert(text):
    lines=text.splitlines();out=[];i=0
    while i<len(lines):
        line=lines[i]
        if line==r'\[':
            block=[line];i+=1
            while lines[i]!=r'\]':block.append(lines[i]);i+=1
            block.append(lines[i]);out.extend(block)
        elif line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                row=[x.strip() for x in lines[i].strip('|').split('|')]
                if not all(re.fullmatch(r'[-: ]+',x) for x in row):rows.append(row)
                i+=1
            i-=1;n=len(rows[0]);spec='lL' if n==2 else 'LLL'
            out.extend([r'\begin{center}',r'\small',r'\begin{tabularx}{\linewidth}{'+spec+'}',r'\toprule'])
            for j,row in enumerate(rows):
                out.append(' & '.join(inline(x) for x in row)+r' \\')
                if j==0:out.append(r'\midrule')
            out.extend([r'\bottomrule',r'\end{tabularx}',r'\end{center}'])
        elif re.match(r'^!\[',line):
            name=Path(re.search(r'\]\((.+)\)',line).group(1)).stem
            macro='esdi'+''.join(x.title() for x in name.split('-'))
            out.append('\\esdiagram{\\'+macro+'}')
        elif line.startswith('#### '):
            out.append(r'\needspace{8\baselineskip}\subsubsection*{'+heading(line[5:])+'}')
        elif line.startswith('### '):
            reserve=4 if line[4:]=='使用时注意' else 6
            out.append(r'\needspace{'+str(reserve)+r'\baselineskip}\subsection{'+heading(line[4:])+'}')
        elif line.startswith('## '):
            out.append(r'\section{'+heading(line[3:])+'}')
        elif line=='**怎么想**':out.append(r'\think')
        elif line.startswith('**方法点睛**：'):
            out.append(r'\insight{'+inline(line.split('：',1)[1])+'}')
        elif line.startswith('**方法'):
            out.append(r'\needspace{6\baselineskip}'+inline(line))
        elif re.match(r'^\d+\. ',line) or line.startswith('- '):
            ordered=not line.startswith('- ');env='enumerate' if ordered else 'itemize'
            pat=r'^\d+\. ' if ordered else r'^- '
            out.append(r'\begin{'+env+'}')
            while i<len(lines) and re.match(pat,lines[i]):
                out.append(r'\item '+inline(re.sub(pat,'',lines[i])));i+=1
            i-=1;out.append(r'\end{'+env+'}')
        else:out.append(inline(line))
        i+=1
    return '\n'.join(out).strip()+'\n'

def section_sources(md):
    headings=['## 关键的八字形','## 例 1','## 例 2','## 辅助线总结']
    starts=[md.index(h) for h in headings]+[len(md)]
    names=['00-key-model','01-example-one','02-example-two','95-summary']
    result={}
    for j,name in enumerate(names):
        body=convert(md[starts[j]:starts[j+1]])
        if j==3:body='\\ifteachernotes\n\\clearpage\n'+body+'\\fi\n'
        result[name+'.tex']='% Synced from content.md by sync_latex.py.\n'+body
    return result

def check_sync():
    # Ignore typesetting whitespace, but never discard teacher edits during a build.
    def lines(s):return [x.strip() for x in s.splitlines() if x.strip()]
    md=(CH/'content.md').read_text(encoding='utf-8')
    for name,expected in section_sources(md).items():
        actual=(SECTIONS/name).read_text(encoding='utf-8')
        if lines(actual)!=lines(expected):
            raise ValueError(f'{name}: TeX/Markdown differ; preserve direct TeX edits and mirror them before building.')

def sync():
    md=(CH/'content.md').read_text(encoding='utf-8')
    for a,b in [('①②③推④',r'$\text{①②③}\Rightarrow\text{④}$'),
                ('①②④推③',r'$\text{①②④}\Rightarrow\text{③}$'),
                ('②③④推①',r'$\text{②③④}\Rightarrow\text{①}$'),
                ('①③④推②',r'$\text{①③④}\Rightarrow\text{②}$')]:md=md.replace(a,b)
    (CH/'content.md').write_text(md,encoding='utf-8')
    SECTIONS.mkdir(parents=True,exist_ok=True)
    for name,body in section_sources(md).items():
        (SECTIONS/name).write_text(body,encoding='utf-8')
    print('PASS: synchronized four LaTeX sections with the Markdown source.')

if __name__=='__main__':sync()
