"""Build and check registered chapters; keep review drafts out of the book."""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
INPUT_RE = re.compile(r"\\input\{([^}]+)\}")
PROBLEM_RE = re.compile(r"\\begin\{problem\}\{\s*题\s*(\d+)")
SOLUTION_RE = re.compile(r"\\begin\{solution\}\{\s*题\s*(\d+)")


def project_path(root, relative):
    """Registry paths are repository-relative and may not escape the checkout."""
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError(f"Expected a repository-relative path: {relative!r}")
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes the repository: {relative}")
    return path


def require_file(root, relative):
    path = project_path(root, relative)
    if not path.is_file():
        raise ValueError(f"Missing file: {relative}")
    return path


def check_pdf_name(name):
    if not isinstance(name, str) or not name.endswith('.pdf') or any(c in name for c in '/\\:'):
        raise ValueError(f"Expected a PDF filename, without a directory: {name!r}")


def load_registry(root):
    registry = json.loads((root / 'chapters.json').read_text(encoding='utf-8'))
    if registry.get('schema_version') != 1:
        raise ValueError('Unsupported chapters.json schema_version.')
    book = registry['book']
    require_file(root, book['main'])
    project_path(root, book['markdown'])
    check_pdf_name(book['pdf'])
    for key in ('title', 'author', 'motto'):
        if not isinstance(book[key], str) or not book[key].strip():
            raise ValueError(f'book.{key} must be a non-empty string.')
    ids, paths, pdfs = set(), set(), {book['pdf']}
    if not registry['chapters']:
        raise ValueError('Register at least one chapter.')
    for chapter in registry['chapters']:
        slug = chapter['id']
        if not re.fullmatch(r'[a-z][a-z0-9-]*', slug) or slug in ids or slug in ('all', 'book'):
            raise ValueError(f'Invalid or duplicate chapter id: {slug}')
        ids.add(slug)
        path = project_path(root, chapter['path'])
        if path.parent != (root / 'chapters').resolve() or path in paths:
            raise ValueError(f'Expected a unique directory directly under chapters/: {path}')
        paths.add(path)
        require_file(root, chapter['path'] + '/content.md')
        require_file(root, chapter['path'] + '/latex/diagrams.tex')
        if chapter['status'] not in ('draft', 'review', 'integrated'):
            raise ValueError(f'{slug}: status must be draft, review, or integrated.')
        count = chapter['problem_count']
        if type(count) is not int or count < 1:
            raise ValueError(f'{slug}: problem_count must be a positive integer.')
        for key in ('title', 'book_title'):
            if not isinstance(chapter[key], str) or not chapter[key].strip():
                raise ValueError(f'{slug}: {key} must be a non-empty string.')
        entry = chapter.get('book_entry')
        if chapter['status'] == 'integrated' and not entry:
            raise ValueError(f'{slug}: integrated chapters need a book_entry.')
        if entry:
            require_file(root, entry)
        standalone = chapter.get('standalone')
        if standalone:
            require_file(root, standalone['main'])
            check_pdf_name(standalone['pdf'])
            if standalone['pdf'] in pdfs:
                raise ValueError(f'Duplicate output PDF: {standalone["pdf"]}')
            pdfs.add(standalone['pdf'])
            if standalone.get('builder'):
                require_file(root, standalone['builder'])
        if not entry and not standalone:
            raise ValueError(f'{slug}: needs a book_entry or standalone main.')
        for script in chapter.get('math_checks', []):
            require_file(root, script)
    if not book_chapters(registry):
        raise ValueError('The book needs at least one integrated chapter.')
    return registry


def book_chapters(registry):
    return [c for c in registry['chapters'] if c['status'] == 'integrated']


def strip_comments(text):
    """Escaped percent signs are text; unescaped percent signs start comments."""
    return re.sub(r'\\[^\n]|%[^\n]*',
                  lambda m: '' if m[0].startswith('%') else m[0], text)


def expanded_tex(project, path, seen=None):
    """Resolve all inputs relative to the XeLaTeX working directory."""
    seen = set() if seen is None else seen
    path = path.resolve()
    if path in seen:
        raise ValueError(f'Repeated or circular input: {path}')
    seen.add(path)
    text = strip_comments(path.read_text(encoding='utf-8'))

    def include(match):
        child = project / match.group(1)
        if not child.suffix:
            child = child.with_suffix('.tex')
        if not child.is_file():
            raise ValueError(f'Missing input: {child} (from {path})')
        child_text = strip_comments(child.read_text(encoding='utf-8'))
        if r'\end{document}' in child_text:
            raise ValueError(f'Unexpected end of document: {child}')
        return expanded_tex(project, child, seen)

    return INPUT_RE.sub(include, text)


def check_pairs(text, chapter):
    problems = Counter(PROBLEM_RE.findall(text))
    solutions = Counter(SOLUTION_RE.findall(text))
    expected = Counter(str(n) for n in range(1, chapter['problem_count'] + 1))
    if problems != expected or solutions != expected:
        raise ValueError(
            f'{chapter["id"]}: expected one problem and one solution for each '
            f'number 1..{chapter["problem_count"]}; '
            f'problems={dict(problems)}, solutions={dict(solutions)}'
        )


def check_chapter(root, registry, chapter, *, for_book=False):
    standalone = chapter.get('standalone')
    if for_book or not standalone:
        entry = require_file(root, chapter['book_entry'])
        project = project_path(root, registry['book']['main']).parent
    else:
        entry = require_file(root, standalone['main'])
        project = entry.parent
    check_pairs(expanded_tex(project, entry), chapter)


def relative_input(project, path):
    relative = Path(os.path.relpath(path, project)).with_suffix('').as_posix()
    return r'\input{' + relative + '}'


def replace_region(text, name, body):
    begin, end = f'% BEGIN GENERATED: {name}', f'% END GENERATED: {name}'
    pattern = re.escape(begin) + r'\n.*?\n' + re.escape(end)
    if len(re.findall(pattern, text, re.S)) != 1:
        raise ValueError(f'Expected exactly one generated region: {name}')
    return re.sub(pattern, lambda _: begin + '\n' + body + '\n' + end, text, flags=re.S)


def book_sources(root, registry):
    book = registry['book']
    chapters = book_chapters(registry)
    main = require_file(root, book['main'])
    tex = main.read_text(encoding='utf-8')
    diagrams = '\n'.join(relative_input(main.parent, project_path(root, c['path'] + '/latex/diagrams.tex'))
                         for c in chapters)
    body = '\n\\clearpage\n'.join(relative_input(main.parent, project_path(root, c['book_entry']))
                                 for c in chapters)
    tex = replace_region(tex, 'chapter-diagrams', diagrams)
    tex = replace_region(tex, 'chapter-body', body)
    drafts = [f'# {book["title"]}\n\n署名：{book["author"]}\n\n{book["motto"]}\n']
    for chapter in chapters:
        draft = require_file(root, chapter['path'] + '/content.md').read_text(encoding='utf-8')
        draft = re.sub(r'^# .*\n', '', draft, count=1)
        draft = re.sub(r'^署名：' + re.escape(book['author']) + r'\s*\n', '', draft, flags=re.M)
        heading = chapter.get('markdown_remove_heading')
        if heading:
            draft = re.sub(r'^\s*## ' + re.escape(heading) + r'\s*\n', '', draft, count=1)
        draft = re.sub(r'^(#{2,5}) ', r'\1# ', draft, flags=re.M)
        draft = re.sub(r'(\]\()(<)?assets/',
                       lambda m: m[1] + (m[2] or '') + chapter['path'] + '/assets/', draft)
        drafts.append(f'## {chapter["book_title"]}\n\n' + draft.strip() + '\n')
    return {main: tex, project_path(root, book['markdown']): '\n'.join(drafts)}


def sync_book(root, registry, *, check_only=False):
    root = root.resolve()
    for path, expected in book_sources(root, registry).items():
        actual = path.read_text(encoding='utf-8') if path.exists() else None
        if actual != expected:
            if check_only:
                raise ValueError(f'Outdated book source: {path.name}; run python scripts/build.py --sync.')
            path.write_text(expected, encoding='utf-8')
            print(f'Updated: {path.relative_to(root)}', flush=True)


def check_book(root, registry):
    sync_book(root, registry, check_only=True)
    main = require_file(root, registry['book']['main'])
    expanded_tex(main.parent, main)
    # Local numbers restart in each chapter; global counters can hide crossed solutions.
    for chapter in book_chapters(registry):
        check_chapter(root, registry, chapter, for_book=True)


def selected_targets(registry, target):
    if target == 'all':
        return [c['id'] for c in book_chapters(registry) if c.get('standalone')] + ['book']
    return [target]


def check_compile_log(project, stem):
    log = (project / f'{stem}.log').read_text(encoding='utf-8', errors='replace')
    patterns = {
        'LaTeX error': r'^!',
        'overfull box': r'Overfull \\[hv]box',
        'missing glyph': r'Missing character:',
        'undefined reference': r'Reference .* undefined|There were undefined references',
    }
    for label, pattern in patterns.items():
        if re.search(pattern, log, re.M):
            raise ValueError(f'{label}; read {project / (stem + ".log")}')
    if not (project / f'{stem}.toc').read_bytes().strip():
        raise ValueError(f'Empty table of contents: {project}')


def compile_main(root, main_relative, pdf_name, engine):
    main = require_file(root, main_relative)
    for i in range(2):
        result = subprocess.run([engine, '-interaction=nonstopmode', '-halt-on-error',
                                 '-file-line-error', main.name], cwd=main.parent,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (main.parent / f'build-pass-{i + 1}.txt').write_bytes(result.stdout)
        if result.returncode:
            print(result.stdout.decode('utf-8', errors='replace'))
            raise ValueError(f'XeLaTeX failed: {main_relative}, pass {i + 1}.')
    check_compile_log(main.parent, main.stem)
    output = root / 'output/pdf' / pdf_name
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(main.with_suffix('.pdf'), output)
    print(f'Built and validated: {output}', flush=True)


def run_math(root, chapters):
    for chapter in chapters:
        for script in chapter.get('math_checks', []):
            print(f'Math check: {chapter["id"]} ({script})', flush=True)
            subprocess.run([sys.executable, str(require_file(root, script))], cwd=root, check=True)


def main(argv=None, *, root=ROOT):
    root = Path(root).resolve()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--xelatex', default='xelatex', help='XeLaTeX executable or full path')
    parser.add_argument('--target', default='all', help='all, book, or a chapter id from --list')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--list', action='store_true', help='List chapter ids, status, and build support')
    modes.add_argument('--check', action='store_true', help='Check sources without compiling or writing')
    modes.add_argument('--sync', action='store_true', help='Update book inputs and combined Markdown only')
    modes.add_argument('--math', action='store_true', help='Run registered mathematical checks only')
    args = parser.parse_args(argv)
    try:
        registry = load_registry(root)
        by_id = {c['id']: c for c in registry['chapters']}
        if args.target not in {'all', 'book', *by_id}:
            raise ValueError(f'Unknown target: {args.target}; use --list.')
        if args.list:
            for chapter in registry['chapters']:
                support = 'standalone PDF' if chapter.get('standalone') else 'book/check/math only'
                print(f'{chapter["id"]}: {chapter["status"]}, {chapter["problem_count"]} problems, {support}')
            print(f'book: {sum(c["problem_count"] for c in book_chapters(registry))} problems')
            return 0
        if args.sync:
            if args.target not in ('all', 'book'):
                raise ValueError('--sync updates the book; omit --target or use --target book.')
            sync_book(root, registry)
            check_book(root, registry)
            print('Book inputs and combined Markdown are synchronized.')
            return 0
        names = selected_targets(registry, args.target)
        if args.math:
            chapters = book_chapters(registry) if args.target in ('book', 'all') else [by_id[args.target]]
            run_math(root, chapters)
            return 0
        if not args.check:
            for name in names:
                if name != 'book' and not by_id[name].get('standalone'):
                    raise ValueError(f'{name}: no standalone main yet; use --target book or --check/--math.')
            engine = shutil.which(args.xelatex)
            if engine is None:
                raise ValueError('XeLaTeX was not found. Use --xelatex to specify its executable path.')
            if 'book' in names:
                sync_book(root, registry)
        for name in names:
            if name == 'book':
                check_book(root, registry)
                if not args.check:
                    compile_main(root, registry['book']['main'], registry['book']['pdf'], engine)
            else:
                chapter = by_id[name]
                check_chapter(root, registry, chapter)
                if not args.check:
                    standalone = chapter['standalone']
                    if standalone.get('builder'):
                        # Preserve chapter-specific exports, including the native editor's review.tex.
                        subprocess.run([sys.executable, str(require_file(root, standalone['builder'])),
                                        '--xelatex', engine], cwd=root, check=True)
                        entry = require_file(root, standalone['main'])
                        check_compile_log(entry.parent, entry.stem)
                        if not (root / 'output/pdf' / standalone['pdf']).is_file():
                            raise ValueError(f'{name}: chapter builder did not produce the registered PDF.')
                    else:
                        compile_main(root, standalone['main'], standalone['pdf'], engine)
            if args.check:
                print(f'Checked: {name}', flush=True)
        return 0
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    raise SystemExit(main())
