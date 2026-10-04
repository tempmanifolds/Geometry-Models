"""Regression checks for chapter isolation and book assembly; no TeX installation needed."""
from collections import Counter
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

BUILD_PATH = Path(__file__).resolve().parents[1] / 'scripts/build.py'
SPEC = importlib.util.spec_from_file_location('project_build', BUILD_PATH)
build = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build)


def paired_text(count):
    return '\n'.join(r'\begin{problem}{题 ' + str(n) + r'}\end{problem}' + '\n' +
                     r'\begin{solution}{题 ' + str(n) + r'}\end{solution}'
                     for n in range(1, count + 1))


class BuildWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.registry = {
            'schema_version': 1,
            'book': {'title': 'Test book', 'author': 'Teacher', 'motto': 'Geometry',
                     'main': 'latex/main.tex', 'markdown': 'content.md', 'pdf': 'book.pdf'},
            'chapters': [],
        }
        for index, (slug, count, status) in enumerate((('alpha', 2, 'integrated'),
                                                     ('beta', 1, 'integrated'),
                                                     ('review', 1, 'review')), 1):
            directory = f'chapters/{index:02}-{slug}'
            entry = f'latex/sections/{slug}.tex' if status == 'integrated' else None
            standalone = {'main': directory + '/latex/main.tex', 'pdf': slug + '.pdf'}
            chapter = {'id': slug, 'path': directory, 'title': slug,
                       'book_title': f'Chapter {index} {slug}', 'status': status,
                       'problem_count': count, 'book_entry': entry,
                       'standalone': standalone, 'math_checks': []}
            self.registry['chapters'].append(chapter)
            self.write(directory + '/content.md', f'# {slug}\n\n![Figure](<assets/figure.png>)\n')
            self.write(directory + '/latex/diagrams.tex', '% Diagram placeholder\n')
            self.write(standalone['main'], paired_text(count))
            if entry:
                self.write(entry, paired_text(count))
        self.write('latex/main.tex', '\n'.join((
            r'\documentclass{article}', '% BEGIN GENERATED: chapter-diagrams', '',
            '% END GENERATED: chapter-diagrams', r'\begin{document}',
            '% BEGIN GENERATED: chapter-body', '', '% END GENERATED: chapter-body',
            r'\end{document}', '',
        )))
        self.save_registry()
        with redirect_stdout(io.StringIO()):
            build.sync_book(self.root, self.registry)

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def save_registry(self):
        self.write('chapters.json', json.dumps(self.registry, ensure_ascii=False))

    def snapshot(self):
        return {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def test_global_counts_cannot_hide_crossed_chapter_solutions(self):
        alpha = (r'\begin{problem}{题 1}\end{problem}' + '\n' +
                 r'\begin{problem}{题 2}\end{problem}' + '\n' +
                 r'\begin{solution}{题 1}\end{solution}' + '\n' +
                 r'\begin{solution}{题 1}\end{solution}')
        beta = (r'\begin{problem}{题 1}\end{problem}' + '\n' +
                r'\begin{solution}{题 2}\end{solution}')
        combined = alpha + '\n' + beta
        # This broken book passes the former global Counter comparison.
        self.assertEqual(Counter(build.PROBLEM_RE.findall(combined)),
                         Counter(build.SOLUTION_RE.findall(combined)))
        self.write('latex/sections/alpha.tex', alpha)
        self.write('latex/sections/beta.tex', beta)
        with self.assertRaisesRegex(ValueError, 'alpha: expected'):
            build.check_book(self.root, self.registry)

    def test_review_is_excluded_from_default_build_and_book_sources(self):
        self.assertEqual(build.selected_targets(self.registry, 'all'), ['alpha', 'beta', 'book'])
        sources = build.book_sources(self.root, self.registry)
        self.assertNotIn('03-review', sources[self.root / 'latex/main.tex'])
        markdown = sources[self.root / 'content.md']
        self.assertNotIn('Chapter 3 review', markdown)
        self.assertIn('(<chapters/01-alpha/assets/figure.png>)', markdown)

    def test_source_checks_need_no_engine_and_write_nothing(self):
        before = self.snapshot()
        with patch.object(build.shutil, 'which', side_effect=AssertionError('must not resolve TeX')):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(build.main(['--check'], root=self.root), 0)
        self.assertEqual(before, self.snapshot())

    def test_standalone_checks_do_not_sync_a_stale_book(self):
        self.write('content.md', 'Book draft that a chapter task must leave alone.\n')
        before = self.snapshot()
        with redirect_stdout(io.StringIO()):
            self.assertEqual(build.main(['--target', 'review', '--check'], root=self.root), 0)
        self.assertEqual(before, self.snapshot())

    def test_sync_accepts_a_noncanonical_windows_temp_directory_path(self):
        # Windows TEMP may use CONNOI~1 while Path.resolve() returns connoisseur.
        self.write('content.md', 'Stale\n')
        with redirect_stdout(io.StringIO()):
            self.assertEqual(build.main(['--sync'], root=Path(self.temp.name)), 0)
        build.check_book(self.root, self.registry)

    def test_new_integrated_chapter_is_assembled_without_editing_python(self):
        review = self.registry['chapters'][2]
        review['status'] = 'integrated'
        review['book_entry'] = 'latex/sections/review.tex'
        self.write(review['book_entry'], paired_text(1))
        self.write(review['path'] + '/content.md', '# review\n\n署名：Teacher\n\nChapter draft\n')
        self.save_registry()
        with redirect_stdout(io.StringIO()):
            self.assertEqual(build.main(['--sync'], root=self.root), 0)
        self.assertIn('sections/review', (self.root / 'latex/main.tex').read_text(encoding='utf-8'))
        self.assertIn('Chapter 3 review', (self.root / 'content.md').read_text(encoding='utf-8'))
        self.assertEqual((self.root / 'content.md').read_text(encoding='utf-8').count('署名：Teacher'), 1)
        before = self.snapshot()
        with redirect_stdout(io.StringIO()):
            self.assertEqual(build.main(['--sync'], root=self.root), 0)
        self.assertEqual(before, self.snapshot())

    def test_outdated_book_is_reported_without_being_overwritten(self):
        self.write('content.md', 'Stale\n')
        with self.assertRaisesRegex(ValueError, 'Outdated book source'):
            build.check_book(self.root, self.registry)
        self.assertEqual((self.root / 'content.md').read_text(encoding='utf-8'), 'Stale\n')

    def test_registry_rejects_duplicate_ids_and_paths_outside_repository(self):
        self.registry['chapters'][1]['id'] = 'alpha'
        self.save_registry()
        with self.assertRaisesRegex(ValueError, 'duplicate chapter id'):
            build.load_registry(self.root)
        with self.assertRaisesRegex(ValueError, 'escapes the repository'):
            build.project_path(self.root, '../outside.tex')

    def test_missing_inputs_and_premature_document_end_are_rejected(self):
        main = self.root / 'chapters/03-review/latex/main.tex'
        self.write('chapters/03-review/latex/main.tex', r'\input{missing}')
        with self.assertRaisesRegex(ValueError, 'Missing input'):
            build.expanded_tex(main.parent, main)
        self.write('chapters/03-review/latex/main.tex', r'\input{child}')
        self.write('chapters/03-review/latex/child.tex', r'\end{document}')
        with self.assertRaisesRegex(ValueError, 'Unexpected end of document'):
            build.expanded_tex(main.parent, main)
        # A commented end marker and literal percent must not trigger false failures.
        self.write('chapters/03-review/latex/child.tex', '% \\end{document}\n' + r'10\% complete')
        self.assertIn(r'10\% complete', build.expanded_tex(main.parent, main))


if __name__ == '__main__':
    unittest.main()
