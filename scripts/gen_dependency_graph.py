# -*- coding: utf-8 -*-
"""Generate graphs/dependency.json from knowledge sidecars + protocol definitions.

Zero-dependency (stdlib only). Per graphs/dependency-graph-schema.json:
nodes = knowledge pages + protocols (+ referenced sources);
edges = dependencies (depends_on) + source_refs (derived_from).
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
KB = BASE / 'knowledge'
PROTO = BASE / 'protocol'
OUT = BASE / 'graphs' / 'dependency.json'


def main():
    nodes, edges = {}, []
    seen_ids = set()

    def add_node(node_id, node_type, label, path):
        if node_id in seen_ids:
            return
        seen_ids.add(node_id)
        nodes[node_id] = {'node_id': node_id, 'node_type': node_type,
                          'label': label, 'metadata': {'path': path}}

    # Knowledge nodes + edges from sidecars
    for f in sorted(KB.glob('*.json')):
        if f.name == 'metadata-schema.json':
            continue
        sc = json.loads(f.read_text(encoding='utf-8'))
        kid = sc.get('knowledge_id', f.stem)
        add_node(kid, 'knowledge', sc.get('title', kid), sc.get('path', f'knowledge/{f.name}'))
        for dep in sc.get('dependencies') or []:
            edges.append({'source': kid, 'target': dep, 'relation': 'depends_on'})
        for ref in sc.get('source_refs') or []:
            add_node(ref, 'source', ref, f'source/{ref}')
            edges.append({'source': kid, 'target': ref, 'relation': 'derived_from'})

    # Protocol nodes
    for f in sorted(PROTO.glob('*.json')):
        proto = json.loads(f.read_text(encoding='utf-8'))
        pid = proto.get('protocol_id', f.stem)
        add_node(pid, 'protocol', proto.get('description', pid), f'protocol/{f.name}')

    graph = {
        'title': 'Dependency Graph — 依赖图',
        'description': '知识/协议/源材料之间的派生与依赖关系。A→B = A depends on B。由 scripts/gen_dependency_graph.py 从 sidecar 与 protocol 定义生成。',
        'version': '0.1.0',
        'generated': '2026-07-17',
        'schema': 'graphs/dependency-graph-schema.json',
        'nodes': list(nodes.values()),
        'edges': edges,
    }
    OUT.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'nodes={len(nodes)} edges={len(edges)} -> {OUT}')


if __name__ == '__main__':
    main()
