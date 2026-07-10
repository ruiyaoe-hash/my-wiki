---
type: source
title: "karpathy/autoresearch README"
description: "Karpathy的自动化AI研究循环项目，给AI一个单GPU训练环境让它自主实验优化"
timestamp: "2026-03-01T00:00:00Z"
created: 2026-07-08
tags: [autoresearch, Karpathy, agent, self-improvement, nanochat]
status: archived
source: https://github.com/karpathy/autoresearch
source_label: karpathy/autoresearch GitHub仓库README (90K+ stars)
---

# autoresearch
(The full README from karpathy/autoresearch - 90K+ stars)

Karpathy March 2026: The idea - give an AI agent a small but real LLM training setup and let it experiment autonomously overnight. It modifies the code, trains for 5 minutes, checks if the result improved, keeps or discards, and repeats. You wake up in the morning to a log of experiments and (hopefully) a better model.

Core files (only 3 that matter):
- prepare.py — fixed constants, one-time data prep, runtime utilities. Not modified.
- train.py — the single file the agent edits. Contains full GPT model, optimizer (Muon + AdamW), training loop. Everything is fair game.
- program.md — baseline instructions for one agent. Point your agent here. This file is edited by the human.

Key design: Fixed 5-minute time budget per experiment. Metric is val_bpb (validation bits per byte). Single GPU (H100 tested). Self-contained with no external dependencies beyond PyTorch. MIT license.

The core insight: you're not touching Python files like a normal researcher. Instead, you're programming the program.md Markdown files that provide context to the AI agents. The default program.md is intentionally bare bones - iterate on it over time to find the "research org code" that achieves fastest progress.
