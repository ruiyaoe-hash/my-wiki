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

        # 4b. 入库标准 v0.1：认知状态字段（本地文件来源应为 T4 + unverified）
        page_fm = self.page_file.read_text(encoding='utf-8-sig')
        self.assertIn('source_tier: T4', page_fm)
        self.assertIn('verification: unverified', page_fm)
        self.assertEqual(sc['source_tier'], 'T4')
        self.assertEqual(sc['verification'], 'unverified')

        # 5. index.md gained the new entry under 新入库
        index = self.index_path.read_text(encoding='utf-8')
        self.assertIn(f'- [[{TITLE}]] — Agent Runtime 自动入库', index)


class TestSourceTierClassification(unittest.TestCase):
    """入库标准 v0.1 来源分级（域名启发式）。"""

    def test_tier_rules(self):
        c = ProtocolExecutor._classify_source_tier
        self.assertEqual(c('https://arxiv.org/abs/2603.07670'), 'T1')
        self.assertEqual(c('https://www.nature.com/articles/x'), 'T1')
        self.assertEqual(c('https://github.com/obra/superpowers'), 'T2')
        self.assertEqual(c('https://deepmind.google/blog/x'), 'T2')
        self.assertEqual(c('https://mp.weixin.qq.com/s/abc'), 'T3')
        self.assertEqual(c('https://zhuanlan.zhihu.com/p/123'), 'T3')
        self.assertEqual(c('some-random-blog.com/post'), 'T4')  # 无 scheme 按本地处理
        self.assertEqual(c('/local/path/article.md'), 'T4')
        self.assertEqual(c(''), 'T4')


class TestExecutorHtmlAndSidecar(unittest.TestCase):
    """Regression for URL-ingest dogfood findings (2026-07-18):
    1. HTML input must be converted to text before summarizing
       (raw HTML produced an empty 要点 section on a real WeChat article).
    2. Sidecar must be parsed from the page's frontmatter, not hardcoded
       defaults (domain/tags/source were previously overwritten).
    """

    def setUp(self):
        # handlers 约定仓库内路径（return 值取相对仓库路径），临时目录放 reports/（已 gitignore）
        self.tmp = Path(tempfile.mkdtemp(prefix='ingest-html-', dir=helpers.BASE_DIR / 'reports'))
        self.html = self.tmp / 'article.html'
        self.html.write_text(
            '<!doctype html><html><head><style>body{color:red}</style>'
            '<script>var x=1;</script></head><body>'
            '<h1>测试文章标题</h1>'
            '<h2>背景</h2><p>这是背景章节的第一句话。这是第二句话。</p>'
            '<h2>方法</h2><p>方法章节内容在这里。还有更多细节。</p>'
            '</body></html>', encoding='utf-8')
        self.page = self.tmp / 'My_Test_Page.md'
        self.page.write_text(
            '---\ntitle: "My Test Page"\ncreated: "2026-07-18"\nupdated: "2026-07-18"\n'
            'type: concept\ndomain: agent-memory-cognition\nstatus: draft\n'
            'source: "some-source"\ntags:\n- alpha\n- beta\n---\n\n# My Test Page\n\n[[LinkA]]\n',
            encoding='utf-8')
        self.sum_out = self.tmp / 'sums'
        self.sc_out = self.tmp / 'sc'

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_html_converted_before_summary(self):
        ex = ProtocolExecutor()
        ex._handle_generate_summary({'input_file': str(self.html), 'output_dir': str(self.sum_out)})
        summary = (self.sum_out / 'article_summary.md').read_text(encoding='utf-8')
        self.assertIn('**背景**', summary)
        self.assertIn('**方法**', summary)
        self.assertIn('这是背景章节的第一句话', summary)
        points = summary.split('## 要点')[1]
        self.assertNotIn('<', points)  # no HTML tags leak into 要点

    def test_sidecar_parsed_from_frontmatter(self):
        ex = ProtocolExecutor()
        ex._handle_generate_sidecar({'page_path': str(self.page), 'output_dir': str(self.sc_out)})
        sc = json.loads((self.sc_out / 'my_test_page.json').read_text(encoding='utf-8'))
        self.assertEqual(sc['domain'], 'agent-memory-cognition')
        self.assertEqual(sc['tags'], ['alpha', 'beta'])
        self.assertEqual(sc['source_refs'], ['some-source'])
        self.assertIn('related', sc)
        self.assertEqual(sc['outgoing_links'], ['LinkA'])


    def test_update_index_creates_missing_index(self):
        """Fresh-clone repos have no index.md (personal content is untracked);
        update_index must create a minimal index instead of silently no-oping."""
        ip = BASE / 'index.md'
        backup = helpers.backup_file(ip)
        try:
            if ip.exists():
                ip.unlink()
            ex = ProtocolExecutor()
            r = ex._handle_update_index({'new_page_title': 'Index Creation Test'})
            self.assertTrue(r['updated'])
            text = ip.read_text(encoding='utf-8')
            self.assertIn('## 新入库', text)
            self.assertIn('[[Index Creation Test]]', text)
        finally:
            helpers.restore_file(ip, backup)


if __name__ == '__main__':
    unittest.main()
