#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""依赖图落盘：knowledge/*.json sidecar → graphs/dependency.json。

节点：每个 sidecar 一个 knowledge 节点（node_id=knowledge_id）；
source_refs 指向的外部来源建 source 节点。
边：
- outgoing_links：wikilink 页面名 → knowledge_id 映射（页面名即 md 文件名
  stem，规则：小写 + 空格→下划线），relation=depends_on；
- source_refs：page → source，relation=derived_from。

断链 = outgoing_links 中无法解析到任何 md 文件 stem 的链接，打印到控制台
（check 协议将来要吃的数据），并随图一起落盘。

输出 graphs/dependency.json：{nodes, edges, stats, broken_links}，
stats = {node_count, edge_count, unresolved_links}。
最后把 graphs/graph-index.json 里 dependency 的 status 改为 data-ready。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = ROOT / 'knowledge'
GRAPH_FILE = ROOT / 'graphs' / 'dependency.json'
INDEX_FILE = ROOT / 'graphs' / 'graph-index.json'
SKIP_DIRS = {'.git', '.obsidian', '.agents', '__pycache__', 'node_modules'}


def norm_name(name):
    """wikilink 页面名 → knowledge_id 规则：取路径末段、小写、空格→下划线。"""
    name = name.split('/')[-1].strip()
    return name.lower().replace(' ', '_')


def collect_md_stems():
    """全库 md 文件名 stem 集合（归一化后），用于判定链接是否断链。"""
    stems = set()
    for p in ROOT.rglob('*.md'):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        stems.add(norm_name(p.stem))
    return stems


def main():
    sidecars = sorted(
        p for p in KNOWLEDGE_DIR.glob('*.json') if p.name != 'metadata-schema.json')

    nodes = {}
    edges = []
    edge_seen = set()
    broken_links = []  # [{from, link}]
    md_stems = collect_md_stems()

    data = {}
    for path in sidecars:
        try:
            sc = json.loads(path.read_text(encoding='utf-8'))
        except Exception as exc:  # noqa: BLE001
            print(f'警告: {path.name} 解析失败，跳过: {exc}')
            continue
        data[sc['knowledge_id']] = sc
        nodes[sc['knowledge_id']] = {
            'node_id': sc['knowledge_id'],
            'node_type': 'knowledge',
            'label': sc.get('title') or sc['knowledge_id'],
            'metadata': {
                'title': sc.get('title'),
                'type': sc.get('type'),
                'domain': sc.get('domain'),
                'sidecar': f'knowledge/{path.name}',
            },
        }

    def add_edge(src, tgt, relation):
        key = (src, tgt, relation)
        if key in edge_seen or src == tgt:
            return
        edge_seen.add(key)
        edges.append({'source': src, 'target': tgt, 'relation': relation})

    def source_node(ref):
        node_id = 'src:' + ref
        if node_id not in nodes:
            nodes[node_id] = {
                'node_id': node_id,
                'node_type': 'source',
                'label': ref,
                'metadata': {},
            }
        return node_id

    for kid, sc in data.items():
        for link in sc.get('outgoing_links', []):
            target = norm_name(link)
            if target in data:
                add_edge(kid, target, 'depends_on')
            elif target not in md_stems:
                broken_links.append({'from': kid, 'link': link})
            # 能解析到非知识页 md（如 源/原文 材料）：不算断链，不出边
        for ref in sc.get('source_refs', []):
            ref = str(ref).strip()
            if ref:
                add_edge(kid, source_node(ref), 'derived_from')

    graph = {
        'nodes': sorted(nodes.values(), key=lambda n: n['node_id']),
        'edges': edges,
        'stats': {
            'node_count': len(nodes),
            'edge_count': len(edges),
            'unresolved_links': len(broken_links),
        },
        'broken_links': broken_links,
    }
    GRAPH_FILE.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'依赖图已写入 {GRAPH_FILE.relative_to(ROOT)}')
    print(f'节点: {len(nodes)}（knowledge {len(data)}，source {len(nodes) - len(data)}）')
    print(f'边: {len(edges)}（depends_on '
          f'{sum(1 for e in edges if e["relation"] == "depends_on")}，derived_from '
          f'{sum(1 for e in edges if e["relation"] == "derived_from")}）')
    print(f'断链: {len(broken_links)}')
    for b in broken_links:
        print(f'  - {b["from"]} -> [[{b["link"]}]]')

    index = json.loads(INDEX_FILE.read_text(encoding='utf-8'))
    index['graphs']['dependency']['status'] = 'data-ready'
    INDEX_FILE.write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('graph-index.json: dependency.status -> data-ready')
    return 0


if __name__ == '__main__':
    sys.exit(main())
