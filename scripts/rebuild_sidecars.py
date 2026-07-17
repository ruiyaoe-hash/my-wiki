#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 md frontmatter 重建 knowledge/*.json sidecar。

裁决：md frontmatter 是唯一事实源，本脚本扫描 知识库/*.md 与
knowledge/pages/*.md，把 frontmatter + 正文 wikilink 萃取为机器可读
sidecar，覆盖写入 knowledge/<文件名小写_空格转下划线>.json。

注意：本脚本为一次性维护脚本，允许使用 PyYAML（若环境已安装）；
运行时代码不得依赖 PyYAML。无 PyYAML 时退回到内置最小解析器。
"""
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = [ROOT / "知识库", ROOT / "knowledge" / "pages"]
OUT_DIR = ROOT / "knowledge"

try:
    import yaml  # noqa: F401
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

# ---------------------------------------------------------------------------
# frontmatter 解析
# ---------------------------------------------------------------------------

def split_frontmatter(text):
    """返回 (frontmatter_text, body)。兼容 BOM 与 --- 前导空格。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return None, text  # 没有闭合 ---，视为无 frontmatter


def _unquote(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        return s[1:-1]
    return s


def _split_inline(inner):
    """按逗号切分行内列表，兼容单/双引号包裹的项。"""
    parts, buf, quote = [], [], None
    for ch in inner:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
        elif ch in ("'", '"'):
            quote = ch
            buf.append(ch)
        elif ch == ",":
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf))
    return [p.strip() for p in parts]


def parse_frontmatter_minimal(fm_text):
    """最小 YAML 子集解析器：key: value、单/双引号字符串、
    块式列表（`tags:\\n- a\\n- b`）、行内列表（`tags: [a, b]`）。
    不支持多行折叠字符串（取首行），仅在无 PyYAML 时使用。"""
    data = {}
    lines = fm_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val == "":
            items = []
            j = i + 1
            while j < len(lines) and re.match(r"^\s*-\s+", lines[j]):
                items.append(_unquote(re.sub(r"^\s*-\s+", "", lines[j])))
                j += 1
            if items:
                data[key] = items
                i = j
                continue
            data[key] = None
        elif val.startswith("[") and val.endswith("]"):
            data[key] = [_unquote(p) for p in _split_inline(val[1:-1]) if p.strip()]
        else:
            data[key] = _unquote(val)
        i += 1
    return data


def parse_frontmatter(fm_text):
    """优先 PyYAML，失败或无 PyYAML 时用最小解析器。返回 (dict, warning)。"""
    if _HAS_YAML:
        try:
            data = yaml.safe_load(fm_text)
            if isinstance(data, dict):
                return data, None
        except Exception as exc:  # noqa: BLE001
            return parse_frontmatter_minimal(fm_text), f"PyYAML 解析失败，已退回最小解析器: {exc}"
        return parse_frontmatter_minimal(fm_text), "frontmatter 非 dict，已退回最小解析器"
    return parse_frontmatter_minimal(fm_text), None

# ---------------------------------------------------------------------------
# 字段萃取
# ---------------------------------------------------------------------------

WIKILINK_RE = re.compile(r"\[\[\s*([^\[\]|#]+?)\s*(?:#[^\[\]|]*)?(?:\|[^\[\]]*)?\]\]")


def extract_outgoing_links(body):
    seen, links = set(), []
    for m in WIKILINK_RE.finditer(body):
        name = m.group(1).strip()
        if name and name not in seen:
            seen.add(name)
            links.append(name)
    return links


def _norm_scalar(v):
    """标量归一：None/空串 -> None；date/datetime -> ISO 日期串；其余 -> str。"""
    if v is None:
        return None
    if isinstance(v, datetime):
        return v.date().isoformat()
    if isinstance(v, date):
        return v.isoformat()
    s = str(v).strip()
    return s if s else None


def _norm_list(v):
    if v is None:
        return []
    if isinstance(v, (list, tuple)):
        return [str(x).strip() for x in v if str(x).strip()]
    return [str(v).strip()]


def parse_date(s):
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def freshness_score(updated_str):
    d = parse_date(updated_str)
    if d is None:
        return None  # 调用方记 0.5 并上报
    days = (date.today() - d).days
    if days <= 90:
        return 1.0
    if days <= 180:
        return 0.7
    if days <= 365:
        return 0.4
    return 0.1


def knowledge_id_for(md_path):
    return md_path.stem.lower().replace(" ", "_")


def sidecar_name_for(md_path):
    return knowledge_id_for(md_path) + ".json"


def first_h1(body):
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None

# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def build_sidecar(md_path):
    text = md_path.read_text(encoding="utf-8-sig")
    fm_text, body = split_frontmatter(text)
    warnings = []
    if fm_text is None:
        fm = {}
        warnings.append("无 frontmatter，使用默认值")
    else:
        fm, warn = parse_frontmatter(fm_text)
        if warn:
            warnings.append(warn)

    rel_path = md_path.relative_to(ROOT).as_posix()
    title = _norm_scalar(fm.get("title")) or first_h1(body) or md_path.stem
    created = _norm_scalar(fm.get("created"))
    updated = _norm_scalar(fm.get("updated"))

    score = freshness_score(updated)
    if score is None:
        score = 0.5
        warnings.append(f"updated 无法解析为日期（值: {updated!r}），freshness_score 记 0.5")

    source_refs = _norm_list(fm.get("source")) + _norm_list(fm.get("source_url"))

    sidecar = {
        "knowledge_id": knowledge_id_for(md_path),
        "title": title,
        "path": rel_path,
        "created": created,
        "updated": updated,
        "type": _norm_scalar(fm.get("type")),
        "domain": _norm_scalar(fm.get("domain")),
        "status": _norm_scalar(fm.get("status")),
        "tags": _norm_list(fm.get("tags")),
        "source_refs": source_refs,
        "related": _norm_list(fm.get("related")),
        "dependencies": [],  # 依赖图人工维护，md 无对应字段，保留键位
        "outgoing_links": extract_outgoing_links(body),
        "freshness_score": score,
    }
    desc = _norm_scalar(fm.get("description"))
    if desc is not None:
        sidecar["description"] = desc
    return sidecar, warnings


def main():
    md_files = []
    for d in SCAN_DIRS:
        md_files.extend(sorted(d.glob("*.md")))

    seen_ids = {}
    collisions = []
    for p in md_files:
        kid = knowledge_id_for(p)
        if kid in seen_ids:
            collisions.append((seen_ids[kid], p))
        seen_ids[kid] = p

    created_files, overwritten, all_warnings, missing_fields = [], [], [], []
    for md_path in md_files:
        sidecar, warnings = build_sidecar(md_path)
        for w in warnings:
            all_warnings.append((md_path.name, w))
        for field in ("title", "created", "updated", "type", "domain", "status"):
            if sidecar.get(field) is None:
                missing_fields.append((md_path.name, field))
        out_path = OUT_DIR / sidecar_name_for(md_path)
        (created_files if not out_path.exists() else overwritten).append(out_path.name)
        out_path.write_text(
            json.dumps(sidecar, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    expected = {sidecar_name_for(p) for p in md_files}
    orphans = sorted(
        p.name for p in OUT_DIR.glob("*.json")
        if p.name not in expected and p.name != "metadata-schema.json"
    )

    print(f"扫描 md 文件: {len(md_files)}（知识库 {len(list((ROOT / '知识库').glob('*.md')))}，"
          f"knowledge/pages {len(list((ROOT / 'knowledge' / 'pages').glob('*.md')))}）")
    print(f"覆盖更新: {len(overwritten)}，新建: {len(created_files)}")
    if created_files:
        print("新建清单:", ", ".join(created_files))
    print(f"孤儿 sidecar（有 json 无 md）: {len(orphans)}")
    for name in orphans:
        print(f"  - {name}")
    if collisions:
        print("knowledge_id 冲突:")
        for a, b in collisions:
            print(f"  - {a} <-> {b}")
    if all_warnings:
        print("解析警告:")
        for fname, w in all_warnings:
            print(f"  - {fname}: {w}")
    if missing_fields:
        print("缺字段清单:")
        for fname, field in missing_fields:
            print(f"  - {fname} 缺 {field}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
