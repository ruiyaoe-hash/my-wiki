---
title: OpenRath
created: '2026-06-24'
updated: '2026-06-24'
type: note
timestamp: '2026-06-25T14:30:00Z'
domain: ai-engineering
status: mature
related:
- '[[多智能体系统]]'
- '[[Session管理]]'
- '[[AI持续学习]]'
tags:
- 开源
- Agent
- 清华
- Session管理
description: 清华大学与中山大学团队开源的多智能体框架，以 Session 为一等公民，提供类 PyTorch 的 Agent 编程体验。
---
## 概述

OpenRath 是清华大学与中山大学 Rath Team 开源的多智能体框架（v1.2.1，BSD-3-Clause，`pip install openrath`），提出以 **Session 为一等公民** 的设计理念。它的核心主张是：别围着 Agent 转了——真正该被当成主角的，是 Agent 干活的记录（Session）。

## 为什么需要 OpenRath

多 Agent 系统跑起来之后，真正麻烦的不是"Agent 之间怎么说话"（AutoGen、CrewAI 已经解决了），而是"说完之后，工作的状态属于谁"：
- 哪个 Agent 在哪条分支上产出了哪个结论？
- 工具调用到底在哪个沙箱里执行的？
- 一次失败重试的完整路径是什么？

聊天记录只能**叙述**这些事，不能**还原**这些事。OpenRath 把 Session 当成"工作证据的载体"，而不只是聊天历史。

### 跟现有框架的本质区别

| 框架 | 解决的问题 |
|------|------|
| AutoGen / CrewAI | Agent 之间**如何通信** |
| LangGraph | Agent 之间**如何路由** |
| OpenRath | 通信和路由之后，**状态归属与控制**——Session 作为控制平面 |

## 架构设计：三大技术支柱

### 支柱一：Agent 是变换层，不是全能助手

Agent 不持有状态。它的核心就是一条路径：`forward(session) -> session`。进水口是 Session，出水口也是 Session，Agent 本身是干的。

这个设计的好处：
- **可堆叠**：Agent -> Compressor -> Agent，像 PyTorch 的层一样任意串联
- **可嵌套**：Workflow 里可以包 Workflow（对应 nn.Module）
- **可替换**：同一种接口下，可以装 Agent 调工具、Compressor 压缩上下文、Memory Agent 存取记忆

```python
from rath import flow
from rath.session import Session

class ReadmeWorkflow(flow.Workflow):
    def __init__(self):
        provider = flow.Provider(model="gpt-5.5")
        self.agent = flow.Agent(
            "Use the word_count tool, then answer briefly.",
            provider, tools=[WordCountTool()], memory="local"
        )
        self.compressor = flow.Compressor(
            "Compress the run into one concise message.", provider
        )

    def forward(self, session: Session) -> Session:
        self.agent.remember_memory("User likes compact summaries.")
        session = self.agent(session)          # Agent 变换
        self.agent.commit_memory(session)      # 记忆提交
        return self.compressor(session)         # 压缩变换
```

### 支柱二：Sandbox 和 Memory 是可插拔后端

**Sandbox**（对应 PyTorch 的 Device）——工具到底在哪运行？通过 `session.to("local", spec="./")` 动态绑定执行环境，支持本地进程、OpenSandbox 容器、以及未来的第三方后端。

**Memory**（对应 PyTorch 的 Parameter）——跨运行保留的记忆。Agent 运行前 `recall`，运行后 `commit`。本地后端用 BM25 检索（零依赖），可选配 OpenViking 外部记忆服务。

解耦的好处：团队已有自己的容器调度和知识库系统，不用推倒重来，包装成 backend 接入即可复用整套 Session/Workflow 抽象。

### 支柱三：Session Graph 是动态图

Session 不是一堆聊天记录，而是一张结构化的 chunk 表，包含四个维度：

| 维度 | 说明 |
|------|------|
| chunks | 有序的上下文行（system/user/assistant/tool_result） |
| placement | 当前 Session 的执行位置（local/opensandbox） |
| lineage | 血缘关系（parent/fork/merge/detach） |
| usage | token 用量统计 |

运行时通过 `fork()`（分叉，保留父链）、`detach()`（切断父链，新根）、`merge()`（合并）实时构建任务图——不需要预先画死流程。这个 define-by-run 特性直接继承自 PyTorch 动态图。

```python
root = Session.from_user_message("Plan a small project.")
forked = root.fork()      # torch.clone() 类比，保留 parent 链
detached = root.detach()  # torch.detach() 类比，切断 parent 链
# Session Graph 可通过 edge_pairs() / ancestors_bfs() 遍历
# 可导出为 JSONL，每一行包含完整 lineage 信息
```

### Selector：模型驱动的动态路由

传统框架把流程写死在代码里。OpenRath 用 Selector——一个 LLM 驱动的路由器——在运行时根据当前 Session 状态，从一组自描述的 Workflow 中选出下一个该跑的：

```python
selector = flow.Selector(provider)
billing = flow.Agent("...", provider, description="Billing, invoices")
tech = flow.Agent("...", provider, description="Installation, errors")
wrapup = flow.Agent("...", provider, description="Wrap up summary")

while not isinstance(
    nxt := selector.forward(session, tech, billing, wrapup),
    flow.EmptyWorkflow
):
    session = nxt(session)
```

用户说"我安装出错了，然后帮我总结一下"——系统自动先路由到 tech Agent，跑完再路由到 wrapup Agent。控制流（if/while）仍然是普通 Python，只有路由决策交给模型。

## MAMS 四象限

OpenRath 从 **Agent 数量 x Session 数量** 两个维度划分多智能体系统：

| 类型 | 定义 | 典型案例 |
|------|------|------|
| 单Agent 单Session | 一个模型处理一条对话 | ChatGPT 式聊天 |
| 多Agent 单Session | 多个角色读写同一份共享状态 | 子代理式协作 |
| 单Agent 多Session | 一个 Agent 管理多个 Session 分支 | OpenClaw 式 session fanout |
| 多Agent 多Session（MAMS） | 多个 Agent 共享多个 Session | **OpenRath 核心目标** |

## 与 PyTorch 的类比

OpenRath 最聪明的一步，是把深度学习开发者最熟悉的那套抽象整搬到了 Agent 系统：

| PyTorch | OpenRath | 含义 |
|---------|----------|------|
| Tensor | Session | 流动的运行时值（chunks + placement + lineage + usage） |
| Device | Sandbox/Backend | 工具运行的执行环境（本地/云/第三方） |
| Parameter | Memory | 持久状态：recall/commit，跨运行保留 |
| Function | Tool | 带模型可见 schema 的可调用操作 |
| nn.Linear | Agent | 可复用的 Session 变换层：forward(session) -> session |
| nn.Module | Workflow | 组合 Agent/Tool/Session 变换的容器 |
| 控制流 | Selector | LLM 驱动的路由器，运行时决定下一个该跑的 Workflow |

这组映射不是噱头。PyTorch 真正教给 OpenRath 的三件事：

1. **Layer 不持有数据** -> Agent 不持有状态（数据是 Tensor，状态是 Session）
2. **Device 可插拔** -> Sandbox/Memory backend 可替换
3. **图是跑起来才长出来的** -> Session Graph 是 define-by-run

## 11 步学习阶梯

官方提供 11 个递进式示例（`example/` 目录），每个只讲一个概念：

| # | 文件 | 概念 | 需 API Key？ |
|---|------|------|:---:|
| 01 | hello_agent | 最小程序：构造 Agent、在 Session 上调用 | 是 |
| 02 | session_lineage | fork/detach、Session Graph、JSONL 导出 | **否** |
| 03 | sandbox_backend | session.to(backend) 切换执行环境 | 是 |
| 04 | tools_builtin | 内置文件/shell 工具 | 是 |
| 05 | custom_tool | 自定义 FlowToolCall | 是 |
| 06 | mcp_tool | 借用 MCP 服务器的工具 | **否** |
| 07 | streaming | 流式输出和 token 统计 | 是 |
| 08 | compress | Compressor 压缩长上下文 | 是 |
| 09 | memory | Memory：remember / recall / commit | **否*** |
| 10 | provider_variation | 换模型厂商 | 是 |
| 11 | dynamic_selector | Selector 动态路由 | 是 |

*09 用本地 memory 后端运行无需 key

## 版本演进

- **v1.1**：解决"持久"——如果单个 Agent 的工作是跨时间展开的，凭什么唯一被保存的只有最终答案？于是有了持久 Session，把干活的证据完整留下。
- **v1.2**：再抬高一层——让 Session 从"单个 Agent 事后可查的记录"升级为"能在多个 Agent 和 Workflow 之间被路由的对象"。

## 关键链接

- GitHub: https://github.com/Rath-Team/OpenRath
- 文档: https://docs.openrath.com
- 官网: https://www.openrath.com
- 博客: https://blog.openrath.com

## 相关阅读

- [[OpenRath：多智能体系统的Session中心化革命——从Agent群聊到运行时控制平面]]
