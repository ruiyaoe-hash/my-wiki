#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""真实 ingest 端到端（狗粮测试）：把 源/原文/ 里一篇未入库材料
《Engram：重新定义AI持续学习，打造企业级智能记忆层.md》走 ingest 协议入库。

验收点（脚本内断言）：
1. 知识页在 知识库/ 生成，带 frontmatter + source 字段 + ## 来源 回链；
2. 源/原文/ 有原文（输入本身），协议另在 source/original/ 存档副本；
3. 源/摘要/ 有结构化摘要，协议另在 source/summaries/ 生成摘要；
4. index.md 新入库区多了该条目。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'state-manager'))
sys.path.insert(0, str(ROOT / 'event-bus'))
sys.path.insert(0, str(ROOT / 'executor'))

from executor import ProtocolExecutor  # noqa: E402

SOURCE = ROOT / '源' / '原文' / 'Engram：重新定义AI持续学习，打造企业级智能记忆层.md'
TITLE = 'Engram 企业级记忆层'
DOMAIN = 'agent-memory-cognition'
TAGS = 'Engram,持续学习,企业记忆,记忆层'


def main():
    assert SOURCE.exists(), f'源文件不存在: {SOURCE}'
    page = ROOT / '知识库' / f'{TITLE.replace(" ", "_")}.md'
    assert not page.exists(), f'知识页已存在，拒绝重复入库: {page}'

    ex = ProtocolExecutor()
    ok = ex.execute('ingest', inputs={
        'url_or_path': str(SOURCE),
        'title': TITLE,
        'domain': DOMAIN,
        'tags': TAGS,
    })
    assert ok, f'ingest 协议执行失败: {ex.state}'

    print('\n=== 验收 ===')
    # 1. 知识页 + frontmatter + 来源回链
    assert page.exists(), f'知识页未生成: {page}'
    text = page.read_text(encoding='utf-8-sig')
    assert text.startswith('---'), 'frontmatter 缺失'
    assert f'title: "{TITLE}"' in text and f'domain: {DOMAIN}' in text
    assert f'source: "{SOURCE.stem}"' in text, 'frontmatter 缺 source 字段'
    assert '## 来源' in text and f'[[{SOURCE.stem}]]' in text, '缺 ## 来源 回链'
    print(f'1. 知识页 OK: {page.relative_to(ROOT)}（含 source + [[{SOURCE.stem}]] 回链）')

    # 2. 原文副本
    copy_en = ROOT / 'source' / 'original' / SOURCE.name
    assert SOURCE.exists() and copy_en.exists()
    assert copy_en.read_text(encoding='utf-8') == SOURCE.read_text(encoding='utf-8')
    print(f'2. 原文 OK: 源/原文/{SOURCE.name}（输入）+ {copy_en.relative_to(ROOT)}（协议存档）')

    # 3. 摘要
    sum_cn = ROOT / '源' / '摘要' / f'{SOURCE.stem}.md'
    sum_en = ROOT / 'source' / 'summaries' / f'{SOURCE.stem}_summary.md'
    assert sum_en.exists(), '协议摘要未生成'
    summary = sum_en.read_text(encoding='utf-8')
    assert '# 摘要' in summary and '## 要点' in summary, '摘要非结构化'
    print(f'3. 摘要 OK: {sum_en.relative_to(ROOT)}（协议生成）'
          + f'，源/摘要/{sum_cn.name} 已存在: {sum_cn.exists()}')

    # 4. index.md 新入库条目
    index = (ROOT / 'index.md').read_text(encoding='utf-8')
    assert f'- [[{TITLE}]] — Agent Runtime 自动入库' in index, 'index.md 未更新'
    print(f'4. index.md OK: 新入库区已有 [[{TITLE}]] 条目')

    print('\nrun_real_ingest: PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
