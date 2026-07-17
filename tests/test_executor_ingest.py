# -*- coding: utf-8 -*-
"""Executor 'ingest' protocol end-to-end test.

Creates a temp markdown source, runs ingest against it, then cleans up
everything it produced (knowledge page, sidecar, original copy, summary)
and restores index.md byte-for-byte.
"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import helpers

from executor import ProtocolExecutor

BASE = helpers.BASE_DIR
TITLE = 'Test Integration Page'
SOURCE_MD = """# 测试集成文章

这是第一段，用来验证摘要不是简单截断。它包含多个句子。第二句在这里。

## 背景

背景章节的正文。Agent Runtime 的 ingest 协议需要结构化摘要。这一句提供额外素材。

## 方法

方法章节的正文，同样包含两句话。用于检查要点提取是否覆盖多个章节。
"""


class TestExecutorIngest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='ingest-test-'))
        self.src = self.tmp / 'test_integration_source.md'
        self.src.write_text(SOURCE_MD, encoding='utf-8')
        # Backup index.md (real working file mutated by the protocol)
        self.index_path = BASE / 'index.md'
        self.index_backup = helpers.backup_file(self.index_path)
        # Artifacts the protocol is expected to produce
        self.original_copy = BASE / 'source' / 'original' / self.src.name
        self.summary_file = BASE / 'source' / 'summaries' / f'{self.src.stem}_summary.md'
        self.page_file = BASE / '知识库' / 'Test_Integration_Page.md'
        self.sidecar_file = BASE / 'knowledge' / 'test_integration_page.json'
        for f in (self.original_copy, self.summary_file, self.page_file, self.sidecar_file):
            if f.exists():
                self.fail(f'pre-existing artifact would be clobbered: {f}')

    def tearDown(self):
        for f in (self.original_copy, self.summary_file, self.page_file, self.sidecar_file):
            if f.exists():
                f.unlink()
        helpers.restore_file(self.index_path, self.index_backup)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_ingest_end_to_end(self):
        ex = ProtocolExecutor()
        ok = ex.execute('ingest', inputs={
            'url_or_path': str(self.src),
            'title': TITLE,
            'tags': 'test,demo',
            'domain': 'knowledge-management',
        })
        self.assertTrue(ok, f'ingest failed: {ex.state}')
        self.assertEqual(len(ex.state), 5)
        for sid, r in ex.state.items():
            self.assertTrue(r.get('success'), f'step {sid} failed: {r}')

        # 1. Original copied into source/original/
        self.assertTrue(self.original_copy.exists())
        self.assertEqual(self.original_copy.read_text(encoding='utf-8'), SOURCE_MD)

        # 2. Structured summary (heading-based), not a raw truncation
        self.assertTrue(self.summary_file.exists())
        summary = self.summary_file.read_text(encoding='utf-8')
        self.assertIn('# 摘要', summary)
        self.assertIn('来源', summary)
        self.assertIn('字数', summary)
        self.assertIn('- **背景**', summary)
        self.assertIn('- **方法**', summary)

        # 3. Knowledge page with YAML frontmatter
        self.assertTrue(self.page_file.exists())
        page = self.page_file.read_text(encoding='utf-8-sig')
        self.assertTrue(page.startswith('---'), 'frontmatter missing')
        self.assertIn(f'title: "{TITLE}"', page)
        self.assertIn('domain: knowledge-management', page)
        self.assertIn('status: draft', page)
        self.assertIn('- test', page)
        self.assertIn('- demo', page)

        # 4. Sidecar JSON
        self.assertTrue(self.sidecar_file.exists())
        sc = json.loads(self.sidecar_file.read_text(encoding='utf-8'))
        self.assertEqual(sc['knowledge_id'], 'test_integration_page')
        self.assertEqual(sc['type'], 'concept')
        self.assertEqual(sc['domain'], 'knowledge-management')
        self.assertEqual(sc['status'], 'draft')

        # 5. index.md gained the new entry under 新入库
        index = self.index_path.read_text(encoding='utf-8')
        self.assertIn(f'- [[{TITLE}]] — Agent Runtime 自动入库', index)


if __name__ == '__main__':
    unittest.main()
