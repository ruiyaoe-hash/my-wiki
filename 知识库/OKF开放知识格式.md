---
title: OKF 开放知识格式
created: '2026-06-24'
updated: '2026-06-24'
type: note
timestamp: '2026-06-25T14:30:00Z'
domain: meta
status: mature
related:
- '[[LLM Wiki模式]]'
- '[[AI驱动知识管理]]'
- '[[工具与人物速查#谷歌]]'
tags:
- OKF
- 标准化
- 知识交换
- 谷歌
description: 谷歌于 2026 年 6 月发布的开放知识格式（v0.1），将卡帕西 LLM Wiki 设想标准化为 Markdown + YAML frontmatter
  的开放规范。
---
## 是什么

OKF（Open Knowledge Format，开放知识格式）是谷歌于 2026 年 6 月 13 日发布的开放规范（v0.1），由 Sam McCreery（Data Analytics Engineering）和 Amit Hormati（BigQuery Engineering）主导。它的本质极其简单：**一个目录，里面是带 YAML frontmatter 的 Markdown 文件，文件之间用普通 Markdown 链接互相指向。**

官网：https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf

## 设计理念

OKF 规范的第一句话就亮明了态度：

> 如果你能 `cat` 一个文件，就能读 OKF；如果你能 `git clone` 一个仓库，就能分发它。

六条设计原则：
1. **人类可读**：不需要任何工具，打开就是 Markdown
2. **Agent 可解析**：不需要私有 SDK，标准 YAML + Markdown 即可
3. **Git 可 diff**：知识变更像代码一样审查、合入、回滚
4. **跨平台可移植**：一个目录，打成 tar 包、挂到任何文件系统、同步到任何工具
5. **渐进式披露**：index.md 逐层导航，Agent 按需深入，不一口吞下整个知识库
6. **最少约定**：只有一个必填字段（type），其余全部可选——够了就行，不多管

## 合规三条件

一个知识包要符合 OKF v0.1 规范，只需满足三条硬性要求：

1. 每个非保留的 `.md` 文件有可解析的 YAML frontmatter
2. 每个 frontmatter 有非空的 `type` 字段
3. 如果有 `index.md` 和 `log.md`，格式符合规定

其余全是软建议：`description`、`resource`、`tags`、`timestamp`——缺了不影响合规，加了价值很大。消费者必须容忍未知 type、缺失字段、断链——这是故意的宽容设计，因为知识包随时在生长、重构、被 Agent 局部生成。

## 核心字段

| 字段 | 必须 | 说明 |
|------|:---:|------|
| `type` | **是** | 概念类型标签，如 BigQuery Table、Metric、Playbook。生产者自选，不注册，消费者必须容错 |
| `title` | 否 | 人类可读的显示名 |
| `description` | 否 | 一句话摘要，用于 index.md 生成和搜索片段 |
| `resource` | 否 | 指向底层数据资产的 URI。抽象概念可省略 |
| `tags` | 否 | 扁平 YAML 列表，用于跨目录分类 |
| `timestamp` | 否 | ISO 8601 格式的最后修改时间 |

## 保留文件名

任何目录层级中，以下文件名有特殊含义，不能用于概念文档：

| 文件名 | 用途 |
|------|------|
| `index.md` | 目录清单，支持渐进式浏览 |
| `log.md` | 按日期记录变更历史 |

## 与 LLM Wiki 的关系

OKF 规范 §10 明确写道：OKF 的灵感来源包括"使用 markdown + frontmatter 的 LLM wiki 仓库"。本质上，OKF 就是卡帕西 LLM Wiki 模式的标准化——把"用 AI 维护知识库"这个实践，从个人作坊升级为行业规范。

区别在于：LLM Wiki 是一个**方法论**（三个操作：Ingest、Query、Lint），OKF 是一个**格式标准**（定义了文件该怎么写、字段该怎么标）。两者互补——用 LLM Wiki 的方法论维护一个 OKF 格式的知识包。

## 生态全景（发布仅两周）

| 项目 | 星 | 做什么 |
|------|:--:|------|
| 官方参考 Agent | - | Python，BigQuery 自动生成 OKF 包 + 交互式 HTML 可视化 |
| OKFy | 32 | npm 包，网站文档转 OKF 包，自带 MCP 服务器，支持自动刷新 |
| okf-knowledge | 26 | Claude Code `/okf` 技能，创建/维护/可视化 OKF 包 |
| okf (superops) | 10 | Go CLI，Git 仓库扫描自动生成 OKF，内置 13 条 lint 规则 |
| okf-tools | - | Python CLI，DuckDB 语义搜索，链接图遍历 |
| okf-conformance | 10 | OKF 合规性校验工具 |
| okf-ingest | - | 统一摄入工具：验证 + 加载到 DuckDB + 语义搜索 |

## 参考

- [[谷歌发布OKF（开放知识格式）：卡帕西LLM-Wiki设想的标准化落地]] — 原始报道
- [[LLM Wiki模式]] — 卡帕西的方法论
- [[AI驱动知识管理]] — AI 维护知识库的实践
