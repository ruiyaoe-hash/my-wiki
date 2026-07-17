#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验 knowledge/*.json sidecar：JSON 可解析、必需键齐全、枚举合法，
并输出 type/domain/status 实际词汇分布与孤儿 sidecar 清单。"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "knowledge"
SCAN_DIRS = [ROOT / "知识库", ROOT / "knowledge" / "pages"]


def main():
    schema = json.loads((OUT_DIR / "metadata-schema.json").read_text(encoding="utf-8"))
    required = schema.get("required", [])
    enums = {
        f: schema["properties"][f].get("enum", [])
        for f in ("type", "domain", "status")
    }

    errors = []
    dist = {f: Counter() for f in ("type", "domain", "status")}
    files = sorted(
        p for p in OUT_DIR.glob("*.json") if p.name != "metadata-schema.json"
    )
    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path.name}: JSON 解析失败: {exc}")
            continue
        for key in required:
            if key not in data:
                errors.append(f"{path.name}: 缺必需键 {key}")
        for field, allowed in enums.items():
            if field in data and data[field] not in allowed:
                errors.append(f"{path.name}: {field}={data[field]!r} 不在枚举内")
            if field in data:
                dist[field][data[field] if data[field] is not None else "(null)"] += 1
        for field in ("tags", "source_refs", "related", "dependencies", "outgoing_links"):
            if field in data and not isinstance(data[field], list):
                errors.append(f"{path.name}: {field} 不是数组")
        score = data.get("freshness_score")
        if not isinstance(score, (int, float)) or not 0 <= score <= 1:
            errors.append(f"{path.name}: freshness_score={score!r} 非法")

    # 孤儿 sidecar / 缺失 sidecar 交叉核对
    expected = set()
    for d in SCAN_DIRS:
        for md in d.glob("*.md"):
            expected.add(md.stem.lower().replace(" ", "_") + ".json")
    actual = {p.name for p in files}
    orphans = sorted(actual - expected)
    missing = sorted(expected - actual)

    print(f"校验 sidecar 文件数: {len(files)}")
    for field in ("type", "domain", "status"):
        print(f"\n[{field}] 实际分布:")
        for value, count in dist[field].most_common():
            print(f"  {value}: {count}")
    print(f"\n孤儿 sidecar（有 json 无 md）: {len(orphans)}")
    for name in orphans:
        print(f"  - {name}")
    print(f"缺失 sidecar（有 md 无 json）: {len(missing)}")
    for name in missing:
        print(f"  - {name}")
    print(f"\n校验错误: {len(errors)}")
    for e in errors:
        print(f"  - {e}")
    return 1 if errors or orphans or missing else 0


if __name__ == "__main__":
    sys.exit(main())
