---
type: summary
title: 翁荔《Harness Engineering for Self-Improvement》摘要
description: 翁荔2026年7月系统性梳理Harness工程与递归式自我提升(RSI)的前沿研究综述
timestamp: "2026-07-08T00:00:00Z"
created: 2026-07-08
tags: [Harness Engineering, RSI, Agent, self-improvement, 上下文工程, 进化搜索]
status: live
source: https://lilianweng.github.io/posts/2026-07-04-harness/
source_label: 翁荔Lilian Weng个人博客原文
related:
  - 源/原文/lilian-weng-harness-engineering-2026-07-04.md
  - 源/原文/wechat-harness-engineering-machine-heart-2026-07-08.md
---

# 摘要

翁荔(Lilian Weng)这篇博客系统梳理了**Harness工程**（围绕基础模型搭建的编排系统）与**递归式自我提升(RSI)**的前沿研究。

## 核心问题

RSI 会先发生在模型权重层面，还是先发生在 Harness 这层"脚手架"上？翁荔的判断：**近期内 RSI 的路径更可能从 Harness 工程开始**，而非模型直接改写权重。

## Harness 三大设计模式

1. **工作流自动化** — 规划→执行→观察→改进的循环（如 Karpathy 的 autoresearch）
2. **文件系统作为持久化记忆** — 不把一切塞进上下文，用文件存日志、diff、实验记录
3. **子智能体与后台任务** — 派生子智能体并行执行，主智能体做进程管理

## Harness 优化路线图

从简单到复杂的演进：指令提示词 → 结构化上下文 → 工作流 → Harness 代码 → 优化器代码

### 上下文工程
- **ACE** (Zhang 2025)：把上下文当不断演化的 playbook，维护条目化的"要点"而非重写整段提示词
- **MCE** (Ye 2026)：双层优化——元层面演化"技能"（机制），基础层面优化具体上下文（内容）
- **Meta-Harness** (Lee 2026)：优化"决定什么信息该被存储和检索"的那段代码本身

### 工作流设计
- **ADAS** (Hu 2025)：元智能体搜索——让 LLM 用代码编写新的智能体工作流
- **AFlow** (Zhang 2025)：用 MCTS（蒙特卡洛树搜索）在图结构中优化工作流
- **AI Scientist** (Lu 2026)、**ScientistOne**、**Autodata**：自动化的完整科研流水线

### 自我提升型 Harness
- **STOP** (Zelikman 2023)：不是改进方案，而是改进"改进器"本身——递归的脚手架自我优化
- **Self-Harness** (Zhang 2026)："弱点挖掘→有边界提议→验证"循环，LLM 智能体改自己的 Harness
- **DGM / Darwin Gödel Machine** (Zhang 2025)：以可编辑 Harness 代码仓库的进化为目标
- **AlphaEvolve** (Novikov 2025)：进化搜索 + LLM 生成 diff，候选程序池不断变异

### 联合优化
- **SIA** (Hebbar 2026)：同时更新 Harness 和模型权重，但证据尚属初步

## 七个关键挑战

1. **弱且模糊的评估者** — 研究品味、新颖性难以量化
2. **上下文与记忆的生命周期** — 随着智能体自主性增长，记忆管理成为核心
3. **负面结果被忽视** — 文献偏向成功，LLM 不擅长"放弃"和"报告失败"
4. **多样性坍缩** — 进化循环趋向已知高回报模式
5. **奖励作弊 (Reward Hacking)** — 评估者和权限控制应独立于 Harness 演化循环
6. **长期成功** — 短视优化难以捕捉可维护性、兼容性等长期指标
7. **人类的角色** — 人应上移，在高抽象层提供监督

## 关键 GitHub 仓库

- **karpathy/autoresearch** (90K+ stars)：单 GPU 自动化 AI 研究循环
- **yasasbanukaofficial/claude-code** (3.6K stars)：Claude Code CLI 开源逆向
