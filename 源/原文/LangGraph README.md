---
source_url: https://raw.githubusercontent.com/langchain-ai/langgraph/main/README.md
source: GitHub langchain-ai/langgraph
type: raw
created: 2026-07-06
tags: [开源, Agent, 工作流, 状态管理, LangGraph, raw]
---

# LangGraph: Low-level orchestration framework for building stateful agents (README)

> GitHub: https://github.com/langchain-ai/langgraph
> Klarna, Replit, Elastic 等使用

核心能力:
- Durable execution: 从失败点自动恢复的持久化执行
- Human-in-the-loop: 在任何执行点检查和修改Agent状态
- Comprehensive memory: 短期工作记忆 + 跨会话长期持久记忆
- Debugging with LangSmith: 可视化追踪Agent行为
- Production-ready deployment: 可扩展的有状态工作流部署

生态: Deep Agents, LangChain, LangSmith, LangSmith Deployment
设计灵感: Pregel, Apache Beam, NetworkX
