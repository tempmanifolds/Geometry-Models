"""Build only the independent review chapter; leave the book unchanged."""
from pathlib import Path
from collections import Counter
import argparse
import re
import shutil
import subprocess

CH=Path(__file__).resolve().parent
ROOT=CH.parents[1]
PROJECT=CH/'latex'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--xelatex',default='xelatex')
args=parser.parse_args()
engine=shutil.which(args.xelatex)
if engine is None:parser.error('XeLaTeX not found; specify --xelatex with its full path.')

def expand(path,seen=None):
    seen=set() if seen is None else seen
    path=path.resolve()
    if path in seen:raise ValueError(f'Repeated input: {path}')
    seen.add(path)
    text=path.read_text(encoding='utf-8')
    text=re.sub(r'(?<!\\)%[^\n]*','',text)
    def child(match):
        p=PROJECT/match.group(1)
        if not p.suffix:p=p.with_suffix('.tex')
        if r'\end{document}' in p.read_text(encoding='utf-8'):
            raise ValueError(f'Unexpected document end: {p}')
        return expand(p,seen)
    return re.sub(r'\\input\{([^}]+)\}',child,text)

text=expand(PROJECT/'main.tex')
# Embed the unchanged Loom class so the native editor needs no extra files.
cls=(PROJECT/'loom.cls').read_text(encoding='utf-8')
license_header=cls.split(r'\NeedsTeXFormat',1)[0]
class_body=cls[cls.index(r'\RequirePackage{geometry}'):].replace(r'\endinput','')
embedded=(license_header+'\n'+r'''\documentclass[11pt]{article}
\makeatletter
\newif\ifloom@letter\loom@letterfalse
\newif\ifloom@cjk\loom@cjktrue
'''+class_body+'\n'+r'\makeatother'+'\n')
review=text.replace(r'\documentclass{loom}',embedded,1)
(CH/'review.tex').write_text('\n'.join(line.rstrip() for line in review.splitlines())+'\n',encoding='utf-8')
problems=Counter(re.findall(r'\\begin\{problem\}\{题\s*(\d+)',text))
solutions=Counter(re.findall(r'\\begin\{solution\}\{题\s*(\d+)',text))
if problems!=solutions or sum(problems.values())!=3:
    raise SystemExit('Expected three paired problems and solutions.')
for i in range(2):
    result=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error',
                           '-file-line-error','main.tex'],cwd=PROJECT,
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (PROJECT/f'build-pass-{i+1}.txt').write_bytes(result.stdout)
    if result.returncode:
        print(result.stdout.decode('utf-8',errors='replace'))
        raise SystemExit(result.returncode)
log=(PROJECT/'main.log').read_text(encoding='utf-8',errors='replace')
for label,pattern in {'LaTeX error':r'^!','overfull box':r'Overfull \\[hv]box',
                      'missing glyph':r'Missing character:',
                      'undefined reference':r'Reference .* undefined'}.items():
    if re.search(pattern,log,re.M):raise SystemExit(f'{label}; read latex/main.log')
if not (PROJECT/'main.toc').read_bytes().strip():raise SystemExit('Empty TOC')
OUT=ROOT/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
target=OUT/'geometry-Models-03-双等腰模型-核对稿.pdf'
shutil.copy2(PROJECT/'main.pdf',target)
print(f'Built and validated independent chapter: {target}')
