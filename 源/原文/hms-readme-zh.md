# HMS Shadow

[English](README.md) | [中文]
(README.zh-CN.md)

HMS Shadow 是一个可复
现的长期记忆问答实验框架。它用
于测试：
在 memory retrieval 之后加�
� answer-time evidence organization，是否�
��让
语言模型更稳定地基于检索到
的记忆完成推理。

项目聚焦 LongMe
mEval 场景。在这类问题中，答案可
能需要同时利用多个
session、多个�
��间点、抽取后的 memory facts，以及
原始 source snippets。

## 一键自动记
忆

HMS 可以直接包装现有 OpenAI clie
nt，让每次模型调用自动执行：

``
`text
用户输入 -> Recall 相关记忆 -> 
注入上下文 -> 调用 LLM
         -> Ret
ain 完整的用户/助手对话
```

在 `.e
nv` 中填写模型 Base URL、API Key 和 Mo
del 后，运行：

```bash
bash scripts/run
_memory_demo.sh
```

脚本会自动启动 Po
stgreSQL 和 HMS，等待 memory API 可用�
�在隔离的 `uv`
环境中安装本地 SDK 
adapter，并运行两轮示例。第一轮�
�存用户偏好和当前项目，
第二轮�
��需要手动调用 `retain()` 或 `recall()
` 就能自动召回这些信息。

这个 d
emo 只需要填写一套 `OPENAI_API_KEY` / 
`OPENAI_BASE_URL` /
`OPENAI_MODEL`。当各�
�色的独立配置仍为空时，脚本会�
�动复用这套配置进行 HMS
推理和 Re
tain 抽取。如果服务不支持 `text-emb
edding-3-small`，需要单独修改
Embeddin
g Model。

应用侧只需要一次包装：


```python
from openai import OpenAI
from hm
s_litellm import wrap_openai

client = wrap_o
penai(
    OpenAI(),
    hms_api_url="http://
127.0.0.1:18080",
    api_key="YOUR_HMS_API_K
EY",
    bank_id="user-alice",
)

response = 
client.responses.create(
    model="gpt-4o-mi
ni",
    input="你记得我当前在做什�
�项目吗？",
)
```

`wrap_openai()` 同时
支持 `client.responses.create(...)` 和
`cl
ient.chat.completions.create(...)`，包括 s
treaming。每个用户应使用稳定且
独
立的 `bank_id`；可以额外设置 `sessio
n_id`，把一段会话累计为一个 HMS �
�档。

## 实验设计

完整复现实验�
��照以下链路执行：

```text
Dataset c
onversations
  -> Retain：抽取并存储结
构化记忆
  -> Recall：针对问题检索
证据
  -> Organize：组织 answer-time evi
dence
  -> Answer：生成 grounded response

  -> Judge：与 gold answer 比较并评分

```

核心思想是：不要直接把松散�
�� retrieved facts 交给回答模型，而�
�在生成前
构造一个中间证据结构�
��把时间、来源、事件状态和数值�
��号显式组织出来。

这套设置适�
�研究以下问题：

- 模型能否跨 ses
sion 连接证据
- 模型能否区分旧状�
��和当前状态
- 模型能否把相对日�
��定位到具体 memories
- 模型能否避�
��重复计数
- 当数值比较缺少一侧�
��据时，模型是否能保守处理

## �
�视化 Demo

项目包含一个不依赖数�
��库的可视化 demo，方便外部读者�
�理解整体架构。它展示了
原始 ret
rieved sessions 如何在 answer generation �
��被组织成 evidence
ledger。

![Memory e
vidence organization demo](docs/assets/memory
_pipeline_demo.svg)

可以直接在浏览器
中打开静态页面：

```text
docs/memory
_pipeline_demo.html
```

这个页面不需�
�模型 key、数据库访问或 benchmark �
�行产物。

## 动态单题回放

仓库�
��包含一个具体的 benchmark-style 单�
�回放。它展示一个 multi-session
问�
�，并动态呈现散落的 session snippets
 如何经过 retrieval、evidence
ledger con
struction、deduplication，最后进入 grou
nded answer generation。

![Dynamic benchmar
k case replay](docs/assets/benchmark_case_rep
lay.svg)

可以直接打开自动播放的�
�放页面：

```text
docs/benchmark_case_re
play.html
```

回放页面会自动推进同
一个案例的 raw session snippets、recall
 candidates、ledger
rows、duplicate-control
 rule、answer packet，以及最终 grounded
 response。

## 实验管线

benchmark 脚�
��暴露两种 pipeline mode。

### Ledger P
ipeline

Ledger pipeline 保持 memory retrie
val 不变，在 answer generation 前加入

结构化证据账本。

对于高风险问�
��类型，ledger 会组织：

- event time

- mention time
- source session 或 document

- fact type
- compact evidence text
- numeric
、date、update signals
- raw source snippet
s，用于 grounding

当你想复现主线 e
vidence organization 实验时，使用这个
模式。

### Self-Evolution Pipeline

Self-
evolution pipeline 保留 ledger pipeline，�
��额外加入一个轻量的
answer-time con
troller。controller 来自错误模式诊断
，主要覆盖：

- count 和 total 去重

- relative-date lookup grounding
- amount 和
 difference calibration
- current 与 previou
s state arbitration

这个模式用于研究
：在 retrieval 之后加入有针对性的�
��制指令，是否会改变或
改善长期
记忆推理行为。

## 目录结构

```te
xt
.
├── .aaaSCRIPT/
│   └── ru
n_benchmark.sh
├── core/
│   ├─�
� dataplane/
│   ├── daemon/
│   �
�── local-suite/
├── deploy/
├─
─ docs/
│   ├── assets/
│   │  
 ├── benchmark_case_replay.svg
│   �
�   └── memory_pipeline_demo.svg
│   
├── benchmark_case_replay.html
│   �
�── memory_pipeline_demo.html
├── i
nterface/
├── lab/
│   └── eval
uation/
│       └── benchmarks/
│  
         ├── common/
│           │ 
  └── benchmark_runner.py
│          
 └── longmemeval/
│               └
── longmemeval_benchmark.py
├── too
ling/
├── .env.example
├── README
.md
└── README.zh-CN.md
```

关键文�
��：

- `.aaaSCRIPT/run_benchmark.sh`：统�
��实验入口脚本
- `scripts/run_memory_de
mo.sh`：一键自动 retain/recall 示例
- 
`examples/automatic_memory/openai_responses.p
y`：两轮 OpenAI Responses API 示例
- `do
cs/benchmark_case_replay.html`：自动播放
的单题过程回放页面
- `docs/assets/be
nchmark_case_replay.svg`：README 中直接�
�示的动态单题回放
- `docs/memory_pipe
line_demo.html`：静态 before/after 可视�
��页面
- `docs/assets/memory_pipeline_demo.
svg`：README 中直接展示的架构示意�
��
- `lab/evaluation/benchmarks/longmemeval/l
ongmemeval_benchmark.py`：LongMemEval pipeli
ne 实现
- `lab/evaluation/benchmarks/common
/benchmark_runner.py`：共享 evaluation run
ner
- `.env.example`：本地配置模板

##
 环境配置

创建本地环境文件：

`
``bash
cp .env.example .env
```

打开 `.env
`，替换所有 `*_change_me`。主要模型
配置位置如下：

| 流程角色 | Base 
URL | API Key | Model |
| --- | --- | --- | -
-- |
| HMS 核心 / Recall 组织 | `HMS_API_
LLM_BASE_URL` | `HMS_API_LLM_API_KEY` | `HMS_
API_LLM_MODEL` |
| Retain / 事实抽取 | `H
MS_API_RETAIN_LLM_BASE_URL` | `HMS_API_RETAIN
_LLM_API_KEY` | `HMS_API_RETAIN_LLM_MODEL` |

| Answer 生成 | `HMS_API_ANSWER_LLM_BASE_UR
L` | `HMS_API_ANSWER_LLM_API_KEY` | `HMS_API_
ANSWER_LLM_MODEL` |
| LLM Judge | `HMS_API_JU
DGE_LLM_BASE_URL` | `HMS_API_JUDGE_LLM_API_KE
Y` | `HMS_API_JUDGE_LLM_MODEL` |
| Embedding 
| `HMS_API_EMBEDDINGS_OPENAI_BASE_URL` | `HMS
_API_EMBEDDINGS_OPENAI_API_KEY` | `HMS_API_EM
BEDDINGS_OPENAI_MODEL` |

这些角色可以�
��用同一个 OpenAI-compatible 服务，此
时在各配置段填写相同的
Base URL �
� API Key 即可。还需要配置：

- `HMS
_API_DATABASE_URL`：可访问且启用 `pgve
ctor` 的 PostgreSQL
- `HMS_DATASET_PATH`：�
��地 LongMemEval 数据集 JSON 路径
- `HM
S_PIPELINE`：`ledger` 或 `self_evolution`


框架会从 `.env` 加载配置。不要把�
��证硬编码到源码里，也不要提交�
��写后的 `.env`。

## 复现逻辑

bench
mark 脚本默认执行完整复现链路：


```text
Retain -> Recall -> Answer -> Judge

```

每个 benchmark item 会先执行 Retai
n，将 conversation sessions 写入记忆库
；
随后针对问题执行 Recall、组织�
��据并生成 Answer；最后由配置的 Ju
dge 模型将
生成答案与 gold answer 进
行比较和评分。

推荐复现流程：


```text
1. 将 .env.example 复制为 .env
2
. 填写数据库、Base URL、API Key、模�
��和数据集路径
3. 先运行 1 到 2 个
 benchmark instances
4. 确认 Retain、Recal
l、Answer、Judge 均成功完成
5. 再提�
��并发和 benchmark 数量
6. 在 .aaaRESUL
T/ 查看结果，在 .aaaLOG/ 查看日志
`
``

只有当数据库中已经存在同一�
� retained memories，并且明确只想重�
�
Recall → Answer → Judge 时，才设置
 `HMS_RETRIEVAL_ONLY=1`。

## 最小端到�
�运行

```bash
cp .env.example .env
# 继�
�之前先编辑 .env。

export HMS_BENCHMAR
K=longmemeval
export HMS_PIPELINE=ledger
expo
rt HMS_RETRIEVAL_ONLY=0
export HMS_MAX_INSTAN
CES=2

bash .aaaSCRIPT/run_benchmark.sh \
  -
-parallel 1 \
  --max-concurrent-questions 1 
\
  --eval-semaphore-size 1
```

干净复现
时，脚本启动后应打印：
`HMS reprod
uction mode: Retain -> Recall -> Judge`。

#
# 运行 Ledger Pipeline

```bash
export HMS_
RETRIEVAL_ONLY=0
export HMS_PIPELINE=ledger
e
xport HMS_MAX_INSTANCES=500
export HMS_SESSIO
N_EXPANSION_WEIGHT=0.5

bash .aaaSCRIPT/run_b
enchmark.sh \
  --parallel 8 \
  --max-concur
rent-questions 8 \
  --eval-semaphore-size 8 
\
  --quiet
```

## 运行 Self-Evolution Pip
eline

```bash
export HMS_RETRIEVAL_ONLY=0
ex
port HMS_PIPELINE=self_evolution
export HMS_M
AX_INSTANCES=500
export HMS_SESSION_EXPANSION
_WEIGHT=0.5

bash .aaaSCRIPT/run_benchmark.sh
 \
  --parallel 8 \
  --max-concurrent-questi
ons 8 \
  --eval-semaphore-size 8 \
  --quiet

```

## 常用运行参数

常用环境变�
��：

- `HMS_PIPELINE`：`ledger` 或 `self_
evolution`
- `HMS_RETRIEVAL_ONLY`：默认是
 `0`；仅在复用已 retained memories 时�
��为 `1`
- `HMS_MAX_INSTANCES`：限制评�
�问题数量
- `HMS_MAX_QUESTIONS`：在筛�
��后继续限制问题数量
- `HMS_DATASET_
PATH`：指定本地 LongMemEval 数据集路
径
- `HMS_SESSION_EXPANSION_WEIGHT`：覆盖
 session expansion weight
- `HMS_PYTHON_BIN`�
��指定 Python 解释器

常用命令行参
数：

- `--parallel`：并发处理的 inst
ance 数量
- `--max-concurrent-questions`：
question-level 最大并发数
- `--eval-sema
phore-size`：evaluator 并发限制
- `--cat
egory`：只运行指定 LongMemEval 类别
-
 `--question-id`：运行一个或多个指�
� question IDs
- `--skip-ingestion`：跳过 
ingestion，使用数据库中的已有 memor
ies
- `--quiet`：减少控制台输出

## �
��地运行产物

实验运行时，本地�
�行产物会写入 ignored directories：

`
``text
.aaaLOG/
.aaaRESULT/
```

这些目录
只用于本地复现，不应提交。


