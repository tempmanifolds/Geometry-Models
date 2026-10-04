"""Build a chapter with two XeLaTeX passes and export its final PDF."""
from pathlib import Path
import argparse
import shutil
import subprocess
import re

ROOT=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--xelatex',default='xelatex',help='XeLaTeX executable or full path')
args=parser.parse_args()
engine=shutil.which(args.xelatex)
if engine is None:
    parser.error('XeLaTeX was not found. Use --xelatex to specify its executable path.')
project=ROOT/'chapters'/'01-half-angle'/'latex'
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
    'overfull box':r'Overfull \[hv]box',
    'missing glyph':r'Missing character:',
    'undefined reference':r'Reference .* undefined',
}
for label,pattern in checks.items():
    if re.search(pattern,log,re.MULTILINE):
        raise SystemExit(f'Build validation failed: {label}. Read main.log.')
out=ROOT/'output'/'pdf';out.mkdir(parents=True,exist_ok=True)
target=out/'geometry-Models-01-夹半角讲义.pdf'
shutil.copy2(project/'main.pdf',target)
print(f'Built and validated: {target}')
