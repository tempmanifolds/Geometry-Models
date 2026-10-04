"""Build the complete handout and/or chapter one with two XeLaTeX passes."""
from pathlib import Path
from collections import Counter
import argparse
import shutil
import subprocess
import re

ROOT=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--xelatex',default='xelatex',help='XeLaTeX executable or full path')
parser.add_argument('--target',choices=('all','book','half-angle'),default='all',
                    help='Build the complete book, chapter one, or both (default).')
args=parser.parse_args()
engine=shutil.which(args.xelatex)
if engine is None:
    parser.error('XeLaTeX was not found. Use --xelatex to specify its executable path.')

def expanded_tex(project, path, seen=None):
    """Resolve inputs relative to the compiler working directory, as XeLaTeX does."""
    seen=set() if seen is None else seen
    path=path.resolve()
    if path in seen:
        raise ValueError(f'Repeated or circular input: {path}')
    seen.add(path)
    text=path.read_text(encoding='utf-8')
    text=re.sub(r'(?<!\\)%[^\n]*','',text)
    def include(match):
        child=project/match.group(1)
        if not child.suffix:child=child.with_suffix('.tex')
        if r'\end{document}' in child.read_text(encoding='utf-8'):
            raise ValueError(f'Unexpected end of document: {child}')
        return expanded_tex(project,child,seen)
    return re.sub(r'\\input\{([^}]+)\}',include,text)

projects={
    'half-angle':(ROOT/'chapters/01-half-angle/latex','geometry-Models-01-夹半角讲义.pdf',10),
    'book':(ROOT/'latex','geometry-Models-讲义.pdf',12),
}
names=('half-angle','book') if args.target=='all' else (args.target,)
out=ROOT/'output/pdf';out.mkdir(parents=True,exist_ok=True)
# The combined Markdown is generated from the separately editable chapter drafts.
drafts=['# geometry Models\n\n署名：Hence\n\n从图形中发现关系，在推理中理解几何\n']
for folder,title in (('01-half-angle','第一章 夹半角'),('02-hand-in-hand','第二章 手拉手模型')):
    draft=(ROOT/'chapters'/folder/'content.md').read_text(encoding='utf-8')
    draft=re.sub(r'^# .*\n','',draft,count=1)
    if folder=='01-half-angle':
        draft=re.sub(r'^\s*## 第一部分 夹半角\s*\n','',draft,count=1)
    draft=re.sub(r'^(#{2,5}) ',r'\1# ',draft,flags=re.M)
    draft=draft.replace('(<assets/',f'(<chapters/{folder}/assets/')
    drafts.append(f'## {title}\n\n'+draft.strip()+'\n')
(ROOT/'content.md').write_text('\n'.join(drafts),encoding='utf-8')
for name in names:
    project,filename,expected=projects[name]
    text=expanded_tex(project,project/'main.tex')
    problems=Counter(re.findall(r'\\begin\{problem\}\{题\s*(\d+)',text))
    solutions=Counter(re.findall(r'\\begin\{solution\}\{题\s*(\d+)',text))
    if problems!=solutions or sum(problems.values())!=expected:
        raise SystemExit(f'{name}: problem/solution pairing failed.')
    for i in range(2):
        completed=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error',
                                  '-file-line-error','main.tex'],cwd=project,
                                 stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        if completed.returncode:
            print(completed.stdout.decode('utf-8',errors='replace'))
            raise SystemExit(completed.returncode)
    log=(project/'main.log').read_text(encoding='utf-8',errors='replace')
    checks={
        'LaTeX error':r'^!',
        'overfull box':r'Overfull \\[hv]box',
        'missing glyph':r'Missing character:',
        'undefined reference':r'Reference .* undefined',
    }
    for label,pattern in checks.items():
        if re.search(pattern,log,re.MULTILINE):
            raise SystemExit(f'{name}: {label}. Read {project}/main.log.')
    if not (project/'main.toc').read_bytes().strip():
        raise SystemExit(f'{name}: missing table of contents.')
    target=out/filename
    shutil.copy2(project/'main.pdf',target)
    print(f'Built and validated: {target} ({expected} problems and solutions)',flush=True)
