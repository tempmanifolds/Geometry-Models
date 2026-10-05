"""Direct teacher edits must survive chapter preparation and mismatch checks."""
from contextlib import redirect_stdout
import importlib.util
import io
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
CH = ROOT / 'chapters/04-eight-shape'

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

sync = load_module('eight_shape_sync', CH / 'sync_latex.py')
with patch.dict('sys.modules', {'sync_latex': sync}):
    chapter_build = load_module('eight_shape_build', CH / 'build.py')

class TeacherEditTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.chapter = self.root / 'chapters/04-eight-shape'
        self.project = self.chapter / 'latex'
        self.project.mkdir(parents=True)
        for source in (CH / 'latex').rglob('*'):
            if source.is_file() and source.suffix in ('.tex', '.cls'):
                target = self.project / source.relative_to(CH / 'latex')
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
        shutil.copy2(CH / 'content.md', self.chapter / 'content.md')
        cls = self.root / 'chapters/01-half-angle/latex/loom.cls'
        cls.parent.mkdir(parents=True)
        shutil.copy2(ROOT / 'chapters/01-half-angle/latex/loom.cls', cls)
        for target, attrs in ((sync, {'CH': self.chapter, 'SECTIONS': self.project / 'sections'}),
                              (chapter_build, {'CH': self.chapter, 'ROOT': self.root,
                                               'PROJECT': self.project})):
            patcher = patch.multiple(target, **attrs)
            patcher.start()
            self.addCleanup(patcher.stop)

    def source_snapshot(self):
        return {p.relative_to(self.chapter): p.read_bytes()
                for p in self.chapter.rglob('*') if p.is_file() and p.name != 'review.tex'}

    def test_prepare_preserves_tex_and_markdown(self):
        before = self.source_snapshot()
        with redirect_stdout(io.StringIO()):
            chapter_build.prepare()
        self.assertEqual(before, self.source_snapshot())
        self.assertTrue((self.chapter / 'review.tex').is_file())

    def test_unmirrored_teacher_edit_stops_without_overwriting(self):
        path = self.project / 'sections/02-example-two.tex'
        path.write_text(path.read_text(encoding='utf-8').replace('二倍关系', '教师新标题'),
                        encoding='utf-8')
        before = self.source_snapshot()
        with self.assertRaisesRegex(ValueError, 'preserve direct TeX edits'):
            chapter_build.prepare()
        self.assertEqual(before, self.source_snapshot())
        self.assertFalse((self.chapter / 'review.tex').exists())

if __name__ == '__main__':
    unittest.main()
