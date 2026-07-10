---
title: MOC 地图笔记法
created: '2026-06-29'
updated: '2026-06-29'
type: note
domain: ai-engineering
status: evergreen
related:
- '[[Zettelkasten 方法]]'
- '[[Evergreen Notes]]'
- '[[知识库跨域架构第一性原理]]'
- '[[LLM Wiki模式]]'
tags:
- lyt
- nick-milo
- obsidian
- navigation
description: Nick Milo 的 Maps of Content 方法：可重组的概念导航页，桥接扁平笔记库与结构化导航——Obsidian 社区跨域组织的标准范式。
---
# MOC 地图笔记法

MOC（Maps of Content）是 Nick Milo 在 Linking Your Thinking (LYT) 框架中提出的概念。它是 Obsidian 社区中被最广泛采纳的跨域导航范式。

## 什么是 MOC？

MOC 是一张"概念地图"——一个笔记页面，不包含原创内容，而是通过 wikilink 将分散的笔记聚合到一个主题下。它不是文件夹，不"拥有"笔记；它只是一组精心编排的入口链接。

## 四个核心特征

1. **不限制访问**：MOC 提供聚焦的入口点，但不阻止从其他路径到达同一篇笔记
2. **鼓励非线性思考**：笔记可以属于多个 MOC，没有层级约束
3. **心理挤压点**：当你感到认知过载时，创建一个 MOC 来收束相关想法
4. **可随时重组**：MOC 可以创建、废弃、重构——不会像文件夹重命名那样破坏链接

## Home Note 模式

LYT 框架用一个 Home note 作为顶层入口，链接到各个主要 MOC。这和我们的 index.md → 域 MOC 页面的设计完全同构。

## MOC 与 Zettelkasten Structure Notes

MOC 本质上是 Zettelkasten 中"Structure Notes"在数字时代的实现。Luhmann 用物理卡片盒完成了 Structure Notes 的编排功能，MOC 用 wikilink 在 Obsidian 中完成同样的功能。

## MOC 与文件夹的对比

| 维度 | 文件夹 | MOC |
|------|--------|-----|
| 笔记归属 | 一篇笔记只能在一个文件夹 | 一篇笔记可以出现在多个 MOC |
| 层级 | 严格树形 | 任意图结构 |
| 重构成本 | 移动=破坏链接 | 修改 MOC 不影响笔记 |
| 跨域 | 一篇笔记跨域时无处可放 | 可在两个域的 MOC 中都出现 |

## 对我们的启示

用 MOC 做域入口，是 Obsidian 生态中被验证的标准方案。我们可以为每个知识域创建一个 MOC 页面（如 [[🏠 AI工程]]、[[🏠 文旅策划]]），每个页面对该域下的所有知识页做主题编排。一篇笔记如果同时涉及 AI 和文旅，两个域的 MOC 都可以链接它。
