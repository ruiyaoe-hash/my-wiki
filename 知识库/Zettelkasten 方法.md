---
title: Zettelkasten 方法
created: '2026-06-29'
updated: '2026-06-29'
type: note
domain: ai-engineering
status: evergreen
related:
- '[[PARA 方法]]'
- '[[Evergreen Notes]]'
- '[[MOC 地图笔记法]]'
- '[[知识库跨域架构第一性原理]]'
- '[[LLM Wiki模式]]'
- '[[KEA架构与知识流转]]'
tags:
- zettelkasten
- method
- pkm
- note-taking
description: Niklas Luhmann 的卡片笔记法：单知识库、原子笔记、概念连接、结构笔记导航——现代 PKM 的源头范式。
---
# Zettelkasten 方法

Zettelkasten（德语"卡片盒"）是德国社会学家 Niklas Luhmann 发明的笔记系统。他用这套系统产出了 50 本专著 + 600+ 篇论文，去世时还有 150 份未完成手稿。

## 三个核心原则

### 1. 原子性 (Atomicity)
每条笔记只包含一个概念。给它一个唯一 ID，内容不超出这个主题的范围。

### 2. 连接性 (Connectivity)
笔记之间通过链接形成网络。全文搜索不够——链接提供了搜索无法提供的信息结构。

### 3. 不要分类，用标签
官方 FAQ 反复强调：**Don't use categories. Use tags instead.** 分类（文件夹层级）是僵化的，标签是灵活的、可叠加的。

## 三层架构

Luhmann 的 Zettelkasten 在尺度增长后自然演化出三层：

1. **Bottom Layer: Content** — 原子笔记本身
2. **Middle Layer: Structure Notes** — 结构笔记，聚合相关内容的导航页
3. **Top Layer: Main Structure Notes + Double Hashes** — 顶层入口 + 特殊标签

这与 MOC（Maps of Content）是同构的——Structure Notes 就是 MOC 的前身。

## 关键决策：一个还是多个 Zettelkasten？

> "How many Zettelkästen should I have? The answer is, most likely, **only one for the duration of your life.**"

Luhmann 本人用一个 Zettelkasten 覆盖了社会学、法学、哲学、政治学等多个领域。他的论点是：最有价值的洞察发生在不同话题的连接点上，而多个 Zettelkasten 会阻断这些连接。

## 收藏家谬误

> Collecting information does not increase your knowledge.

仅仅收集、存档、摘录不产生知识。必须用自己的话重写、连接、综合。

## 对我们的启示

| Zettelkasten | 我们的 Wiki |
|---|---|
| Inbox | _raw/ |
| Note Archive | 知识库/ |
| Reference Manager | 原始资料/ |
| Structure Notes | index.md + MOC 页面 |
| Buffer Notes | hot.md |

我们已有的架构与 Zettelkasten 高度同构。多域扩展只需要让 MOC 页面承担域入口的角色，不需要拆分成多个 vault。
