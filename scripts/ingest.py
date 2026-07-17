#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ingest CLI：把一篇外部材料（URL 或本地文件）走 ingest 协议入库。

用法 / Usage:
    python scripts/ingest.py <url_or_path> --title "标题" [--domain DOMAIN] [--tags a,b]

示例 / Example:
    python scripts/ingest.py ./article.md --title "我的新页" --domain knowledge-management --tags demo
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'state_manager'))
sys.path.insert(0, str(ROOT / 'event_bus'))
sys.path.insert(0, str(ROOT / 'executor'))

from executor import ProtocolExecutor  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser(description='Ingest external content into the knowledge base')
    parser.add_argument('url_or_path', help='URL or local file path')
    parser.add_argument('--title', required=True, help='knowledge page title')
    parser.add_argument('--domain', default='knowledge-management',
                        help='domain value (must exist in knowledge/metadata-schema.json enum)')
    parser.add_argument('--tags', default='', help='comma-separated tags')
    args = parser.parse_args(argv)

    ex = ProtocolExecutor()
    ok = ex.execute('ingest', inputs={
        'url_or_path': args.url_or_path,
        'title': args.title,
        'domain': args.domain,
        'tags': args.tags,
    })
    if not ok:
        print(f'ingest FAILED: {ex.state}')
        return 1
    print(f'ingest OK: 知识库/{args.title.replace(" ", "_")}.md（已更新 index.md）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
