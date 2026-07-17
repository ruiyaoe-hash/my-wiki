# Quickstart — 5 分钟上手 / 5-Minute Quickstart

以下命令全部经过实机验证。/ All commands below are verified on a real machine.

## 1. 安装 / Install

```bash
git clone https://github.com/ruiyaoe-hash/my-wiki.git
cd my-wiki
pip install -e .        # 提供 agent-runtime 命令；也可以不装，直接用 python 调脚本
```

要求：Python ≥ 3.10，无第三方依赖。/ Requires Python ≥ 3.10. Zero third-party dependencies.

## 2. 第一次运行 / First Run

```bash
agent-runtime                      # 等价于 python agents/wiki_agent.py
```

效果：Planner 开一个 session → 出队一个 check 任务 → Executor 跑 `protocol/check.json`
→ 生成 `reports/check-<日期>.md` → 事件追加到 `event_bus/history/events.jsonl`
→ `state/execution-status.json` 计数 +1。

## 3. 放入你的知识页 / Add Your Knowledge

在 `知识库/` 下新建任意 Markdown，带 YAML frontmatter：

```markdown
---
title: "我的第一页"
created: "2026-07-18"
updated: "2026-07-18"
type: concept
domain: knowledge-management
status: draft
tags: [demo]
---

# 我的第一页

正文，支持 [[双向链接]]。
```

然后重建机器可读 sidecar 并校验：

```bash
python scripts/rebuild_sidecars.py
python scripts/validate_sidecars.py
```

## 4. 入库一篇外部材料 / Ingest External Content

```bash
python scripts/ingest.py ./article.md --title "文章标题" --domain knowledge-management --tags demo
```

协议五步自动完成：抓原文（`source/original/`）→ 结构化摘要（`source/summaries/`）
→ 知识页（`知识库/`，带 source 回链）→ sidecar（`knowledge/`）→ 更新 index。

设置环境变量 `AGENT_RUNTIME_LLM_BASE_URL` + `AGENT_RUNTIME_LLM_API_KEY` 后，
摘要改用 OpenAI 兼容 LLM 生成；未设置时使用内置提取式摘要，全程离线。

## 5. 让它自己跑 / Let It Run

```bash
agent-runtime --loop 10 --interval 60    # 连续 10 轮，每轮间隔 60 秒
agent-runtime --recover                  # 上次被 kill？先恢复再跑
```

## 6. 验证一切正常 / Verify

```bash
python -m unittest discover tests        # 测试套件全绿即正常
```

## 下一步 / Next

- 自定义协议：复制 `protocol/TEMPLATE.json`，参考 `CONTRIBUTING.md`
- 组件接口：各组件目录下的 `INTERFACE.md`
- 架构说明：`README.md` + `ontology/ontology.md`
