---
source_url: https://raw.githubusercontent.com/topoteretes/cognee/main/README.md
source: GitHub topoteretes/cognee
type: raw
created: 2026-07-06
tags: [开源, Agent记忆, 知识图谱, Cognee, raw]
---

# Cognee: The Open-Source AI Memory Platform for Agents (README)

> GitHub: https://github.com/topoteretes/cognee
> 研究论文: https://arxiv.org/abs/2505.24478

## 核心定位
开源 AI 记忆平台，为 AI Agent 提供持久长期记忆。支持任何格式的数据摄入，自动构建自托管知识图谱。

## 四个核心操作
- remember: 永久存储到知识图谱
- recall: 查询检索
- forget: 删除
- improve: 持续优化

## 架构特色
- 整个记忆层可以运行在单个 Postgres 实例上（图+向量+会话+元数据）
- 支持本地开发: SQLite, LanceDB, Kuzudb
- 开源 Benchmark: BEAM（100K tokens: 0.79, 10M tokens: 0.67）
- 提供 Claude Code 插件、MCP server、Rust/TypeScript 客户端

## 部署选项
- Cognee Cloud: 托管服务
- Docker Compose / Docker 预构建镜像
- Modal / Railway / Fly.io / Render / Daytona
