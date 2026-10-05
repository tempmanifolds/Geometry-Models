"""Validate/build the standalone examples; leave the book registry and sources unchanged."""
from pathlib import Path
import argparse
import re
import shutil
import subprocess
import sys
from sync_latex import check_sync

CH=Path(__file__).resolve().parent
ROOT=CH.parents[1]
PROJECT=CH/'latex'

def expand(path):
    text=path.read_text(encoding='utf-8')
    def child(m):
        p=PROJECT/m.group(1)
        if not p.suffix:p=p.with_suffix('.tex')
        if r'\end{document}' in p.read_text(encoding='utf-8'):
            raise ValueError(f'Unexpected document end: {p}')
        return expand(p)
    return re.sub(r'\\input\{([^}]+)\}',child,text)

def prepare():
    check_sync()
    text=expand(PROJECT/'main.tex')
    assert text.count(r'\end{document}')==1
    assert len(re.findall(r'\\section\{\\texorpdfstring\{例 \$[12]\$',text))==2
    assert len(re.findall(r'\\Rightarrow',text))==4
    assert '集中解析' not in text and '∠2' not in text
    cls=(ROOT/'chapters/01-half-angle/latex/loom.cls').read_text(encoding='utf-8')
    header=cls.split(r'\NeedsTeXFormat',1)[0]
    body=cls[cls.index(r'\RequirePackage{geometry}'):].replace(r'\endinput','')
    embedded=(header+'\n'+r'''\documentclass[11pt]{article}
\makeatletter
\newif\ifloom@letter\loom@letterfalse
\newif\ifloom@cjk\loom@cjktrue
'''+body+'\n'+r'\makeatother'+'\n')
    review=text.replace(r'\documentclass{loom}',embedded,1)
    (CH/'review.tex').write_text('\n'.join(x.rstrip() for x in review.splitlines())+'\n',encoding='utf-8')
    print('PASS: standalone examples and self-contained editor source prepared.')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--xelatex',default='xelatex')
    args=parser.parse_args()
    prepare()
    subprocess.run([sys.executable,str(CH/'check_math.py')],check=True)
    if args.check:return
    engine=shutil.which(args.xelatex)
    if engine is None:parser.error('XeLaTeX not found; specify --xelatex.')
    for i in range(2):
        result=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error',
                               '-file-line-error','main.tex'],cwd=PROJECT,
                              stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (PROJECT/f'build-pass-{i+1}.txt').write_bytes(result.stdout)
        if result.returncode:
            print(result.stdout.decode('utf-8',errors='replace')[-7000:])
            raise SystemExit(result.returncode)
    log=(PROJECT/'main.log').read_text(encoding='utf-8',errors='replace')
    for label,pat in {'LaTeX error':r'^!','overfull box':r'Overfull \\[hv]box',
                      'missing glyph':r'Missing character:',
                      'undefined reference':r'Reference .* undefined'}.items():
        if re.search(pat,log,re.M):raise SystemExit(f'{label}; read latex/main.log')
    assert (PROJECT/'main.toc').read_bytes().strip(),'Empty TOC'
    out=ROOT/'output/pdf/geometry-Models-04-八字形模型-核对稿.pdf'
    out.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(PROJECT/'main.pdf',out)
    print(f'PASS: built and validated {out}')

if __name__=='__main__':main()
