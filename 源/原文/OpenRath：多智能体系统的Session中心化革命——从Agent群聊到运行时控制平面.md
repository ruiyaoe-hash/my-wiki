# OpenRath：多智能体系统的Session中心化革命——从Agent群聊到运行时控制平面

> 来源: 得到大脑 · 创建: 2026-06-18

### **🚩 核心问题：Agent集群的管理困境**

**多智能体系统的扩展性挑战**
- **状态碎片化**：每个Agent独立维护上下文，导致数据冗余与不一致。
- **协作黑箱化**：任务分支与推理路径缺乏追踪，难以复现与调试。
- **环境隔离**：模型调用、工具执行、沙箱环境状态各自独立，系统扩展至百级Agent时失控。

**解决方案**：清华大学与中山大学团队（Rath Team）开源**OpenRath**，提出以**Session为一等公民**的设计理念，替代传统Agent为中心的架构，实现多Agent共享状态与可控协作。

### **🔍 Session核心架构解析**

#### **(一) Session Graph：数据流的分叉与合并**

![Session Graph架构图](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb9b89b7f08a65dc88cbcd4026bdc897c?Expires=1784363335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=bnyvYfQ4JmgEsMRLCC6%2FlRqVGVQ%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)
- **Initial Session**：包含上下文、placement（执行位置）、lineage（血缘关系）、usage（使用统计）的初始状态。
- **Fork（分叉）**：复制并延展Session分支，支持并行任务处理（如Research、Code、Review分支）。
- **Merge（合并）**：汇总多分支结果，形成包含完整上下文、血缘记录、统一结果的Final Session。
- **Sandbox Backend**：工具执行环境，支持本地（Local Backend）、云沙箱（OpenSandbox）及第三方后端。

#### **(二) 核心特性与术语**

| 特性 | 定义 | 作用 |
| :--- | :--- | :--- |
| **Lineage** | 追踪结果来源（角色/分支/工具） | 实现可追溯性与审计能力 |
| **Placement** | 记录工具执行位置 | 确保环境一致性，避免状态漂移 |
| **FlowToolCall** | 绑定模型可见接口与实际执行逻辑 | 统一工具调用标准，支持MCP协议适配 |

### **🤖 Agent Cluster：专业化协作范式**

#### **(一) 多Agent分工模型**

![Agent Cluster协作示意图](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F77c02b995beabf84f3111b23f5d73997?Expires=1784363335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=J%2BG0HuD%2F6JPpQBJR%2FYBIIic7eUU%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)
- **Planner**：任务拆解与规划。
- **Researcher**：信息检索与资料分析。
- **Coder**：代码实现与调试。
- **Reviewer**：结果审查与错误修正。
- **Executor**：工具执行与环境操作。
- **Memory Agent**：长期记忆管理（向量库/知识库）。

#### **(二) 共享Session机制**
- **核心思想**：系统能力来自多个专业Agent的协作，而非单个超级Agent。
- **协作流程**：各Agent读取Shared Session状态→完成局部任务→将结果写回Session，形成接力式工作流。

### **🔄 MAMS范式：多Agent多Session协同**

#### **(一) 智能体系统四象限分类**

![MAMS范式示意图](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbcb903d1f5f5241b3becda9dc56b7e6d?Expires=1784363335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2qLsrIZiXeSrh4BSRjCa%2BwOQAT4%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)

| 类型 | 定义 | 典型案例 |
| :--- | :--- | :--- |
| **单Agent单Session** | 单个Agent围绕单个会话 | ChatGPT式对话 |
| **多Agent单Session** | 多个Agent共享一个会话 | 多角色共享上下文 |
| **单Agent多Session** | 单个Agent管理多个分支 | OpenClaw分支扇出 |
| **多Agent多Session（MAMS）** | 多个Agent协作多个会话 | OpenRath核心目标 |

#### **(二) 与现有框架的本质差异**
- **AutoGen/CrewAI**：解决Agent之间**如何通信**。
- **LangGraph**：解决Agent之间**如何路由**。
- **OpenRath**：解决Agent通信后**状态归属与控制**，提出Session作为控制平面的核心地位。

### **🔧 OpenRath技术架构：PyTorch式抽象映射**

#### **(一) 核心概念对应关系**

![OpenRath与PyTorch抽象映射](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F783deefdd4d966583663f0ed8f8786f9?Expires=1784363335&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ZTi2Xg3gWr0OSyGPkLXC76tPE%2BY%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)

| PyTorch | 映射 | OpenRath | 说明 |
| :--- | :--- | :--- | :--- |
| **Tensor** | → | **Session** | 流动的运行时状态（上下文/血缘/位置） |
| **Device** | → | **Sandbox/Backend** | 工具执行环境（本地/云/第三方） |
| **Parameter** | → | **Memory** | 持久化Agent状态（可recall/commit） |
| **Function** | → | **Tool** | 模型可见的操作接口 |
| **nn.Linear** | → | **Agent** | Session变换层（forward(session)→session） |
| **nn.Module** | → | **Workflow** | 组合Agent/Tool的子工作流 |

#### **(二) 三大技术支柱**
1. **Agent作为变换层**  
   - 无状态设计：Agent不持有数据，仅通过`forward(session)`接口转换Session。  
   - 可组合性：支持堆叠（如Agent+Compressor）与嵌套，形成复杂Workflow。

2. **可插拔后端**  
   - **Sandbox**：通过`session.to("local"/"opensandbox")`动态切换执行环境。  
   - **Memory**：支持本地文件（BM25检索）、向量库、OpenViking外部服务。

3. **动态Session Graph**  
   - 运行时生成：通过fork/merge实时构建任务分支，无需预先定义流程。  
   - 血缘追踪：记录每步操作来源，支持回滚、审计与问题定位。

### **💻 快速上手：核心代码示例**

#### **(一) 最小工作流**
```python
from rath import flow
from rath.session import Session

class ReadmeWorkflow(flow.Workflow):
    def __init__(self):
        provider = flow.Provider(model="gpt-5.5")
        self.agent = flow.Agent(  # Agent变换层
            "Use the `word_count` tool, then answer briefly.",
            provider, tools=[WordCountTool()], memory="local"
        )
        self.compressor = flow.Compressor(  # 压缩变换层
            "Compress the run into one message.", provider
        )

    def forward(self, session: Session) -> Session:
        self.agent.remember_memory("User likes compact summaries.")  # 记忆操作
        session = self.agent(session)  # 执行Agent变换
        self.agent.commit_memory(session)  # 提交记忆
        return self.compressor(session)  # 执行压缩变换

# 初始化Session并指定执行环境
session = Session.from_user_message("Count words in: OpenRath makes agent clusters traceable.")
session = session.to("local", spec="./")  # 绑定本地沙箱
out = ReadmeWorkflow()(session)  # 运行工作流
```
#### **(二) 动态路由（Selector）**
```python
selector = flow.Selector(provider)
while not isinstance(
    nxt := selector.forward(session, triage, tech, wrapup),  # 模型驱动路由
    flow.EmptyWorkflow
):
    session = nxt(session)  # 动态执行下一个Workflow
```
### **📈 版本与生态**
- **当前版本**：v1.2.1（PyPI）  
- **开源协议**：BSD-3-Clause  
- **安装方式**：`pip install openrath`（基础版）；`pip install "openrath[opensandbox]"`（含容器沙箱）  
- **学习资源**：11个递进式示例（`example/`目录），覆盖从基础Agent调用到动态协作。

### **🎯 关键洞察**
1. **从Prompt工程到系统工程**：OpenRath将Agent开发从提示词拼接升级为模块化组件设计，类比PyTorch对深度学习的工程化革新。  
2. **证据链优先**：强调Session作为「工作证据载体」，而非单纯聊天记录，满足生产级系统的可追溯性需求。  
3. **解耦设计**：通过Sandbox/Memory可插拔后端，支持企业复用现有容器调度与知识库系统，降低迁移成本。  
4. **动态图优势**：Session Graph运行时生成特性，使Agent协作流程从「写死剧本」升级为「智能路由」，适配复杂任务的不确定性。
