<div align="center">

<img src="docs/assets/b
randing/hms-hero.png" alt="Holographic Memory
 System" width="94%">

### Structured Memory 
Intelligence for Reliable Long-Horizon Reason
ing

<table>
  <tr>
    <td valign="middle"><
strong>ShadowWeave Team</strong></td>
    <td
 width="74" align="center" valign="middle">
 
     <img src="docs/assets/branding/shadowwea
ve-mark.png" alt="ShadowWeave" width="62">
  
  </td>
  </tr>
</table>

<a href="https://ar
xiv.org/"><img src="https://img.shields.io/ba
dge/arXiv-coming_soon-B31B1B?style=flat-squar
e&logo=arxiv&logoColor=white" alt="arXiv: com
ing soon"></a>
<img src="https://img.shields.
io/badge/status-active-145DA0?style=flat-squa
re" alt="Project status: active">

[English](
README.md) · [中文](README.zh-CN.md)

</di
v>

---

## Abstract

The **Holographic Memor
y System (HMS)** is a reproducible long-term 
memory QA
framework for studying whether stru
ctured answer-time evidence organization can

improve a language model's reasoning over ret
rieved memories.

The project focuses on the 
LongMemEval setting, where a question may req
uire
evidence from multiple sessions, timesta
mps, extracted memory facts, and raw
source s
nippets.

## One-Command Automatic Memory

HM
S can wrap an existing OpenAI client so each 
model call automatically:

```text
user input
 -> Recall relevant memories -> inject contex
t -> call the LLM
           -> Retain the co
mpleted user/assistant exchange
```

Configur
e the model Base URL, API key, and model in `
.env`, then run:

```bash
bash scripts/run_me
mory_demo.sh
```

The script starts PostgreSQ
L and HMS locally, waits for the memory API, 
installs
the local SDK adapter in an isolated
 `uv` environment, and runs a two-turn demo.

The first turn stores a preference and projec
t; the second turn recalls both
without manua
lly calling `retain()` or `recall()`.

For th
is demo, one `OPENAI_API_KEY` / `OPENAI_BASE_
URL` / `OPENAI_MODEL` set is
enough. The scri
pt reuses it for HMS reasoning and retain ext
raction when the
role-specific values remain 
unset. Set the embedding model separately whe
n your
provider does not support `text-embedd
ing-3-small`.

The application-side integrati
on is one wrapper call:

```python
from opena
i import OpenAI
from hms_litellm import wrap_
openai

client = wrap_openai(
    OpenAI(),
 
   hms_api_url="http://127.0.0.1:18080",
    
api_key="YOUR_HMS_API_KEY",
    bank_id="user
-alice",
)

response = client.responses.creat
e(
    model="gpt-4o-mini",
    input="What d
o you remember about my current project?",
)

```

`wrap_openai()` supports both `client.re
sponses.create(...)` and
`client.chat.complet
ions.create(...)`, including streaming. Use a
 stable,
per-user `bank_id`; optionally set `
session_id` to accumulate one conversation
as
 a tracked HMS document.

## Experiment Desig
n

The reproducible evaluation follows one co
mplete pipeline:

```text
Dataset conversatio
ns
  -> Retain: extract and store structured 
memories
  -> Recall: retrieve evidence for e
ach question
  -> Organize: build an answer-t
ime evidence structure
  -> Answer: generate 
a grounded response
  -> Judge: compare the r
esponse with the gold answer
```

The core id
ea is to avoid giving the answer model a loos
e list of retrieved
facts. Instead, the syste
m builds an intermediate evidence structure t
hat makes
time, source, event state, and nume
ric signals explicit before generation.

This
 setup is useful for studying questions such 
as:

- whether the model can connect evidence
 across sessions
- whether the model can dist
inguish old and current user states
- whether
 the model can ground relative dates to concr
ete memories
- whether the model can avoid du
plicate counting
- whether missing numeric si
des are handled conservatively

## Visual Dem
o

The project includes a database-free demo 
for external readers. It shows how
raw retrie
ved sessions are converted into an organized 
evidence ledger before
answer generation.

![
Memory evidence organization demo](docs/asset
s/memory_pipeline_demo.svg)

Open the standal
one demo page:

```text
docs/memory_pipeline_
demo.html
```

This page can be viewed direct
ly in a browser and does not require model ke
ys,
database access, or benchmark artifacts.


## Dynamic Case Replay

The repository also 
includes a concrete benchmark-style case repl
ay. It shows a
single multi-session question 
and animates how scattered session snippets m
ove
through retrieval, evidence ledger constr
uction, deduplication, and grounded
answer ge
neration.

![Dynamic benchmark case replay](d
ocs/assets/benchmark_case_replay.svg)

Open t
he auto-playing replay page:

```text
docs/be
nchmark_case_replay.html
```

The replay page
 auto-advances through the raw session snippe
ts, recall candidates,
ledger rows, duplicate
-control rule, answer packet, and final groun
ded response
for the same case.

## Pipelines


Two pipeline modes are exposed through the 
benchmark script.

### Ledger Pipeline

The l
edger pipeline keeps memory retrieval unchang
ed and adds a structured
evidence ledger befo
re answer generation.

For high-risk question
 types, the ledger records:

- event time
- m
ention time
- source session or document
- fa
ct type
- compact evidence text
- numeric, da
te, and update signals
- raw source snippets 
for grounding

Use this mode when you want to
 reproduce the main evidence-organization
exp
eriment.

### Self-Evolution Pipeline

The se
lf-evolution pipeline keeps the ledger pipeli
ne and adds a lightweight
answer-time control
ler. The controller is driven by diagnosed fa
ilure patterns:

- count and total deduplicat
ion
- relative-date lookup grounding
- amount
 and difference calibration
- current versus 
previous state arbitration

This mode is inte
nded for studying whether targeted control in
structions can
improve or change memory reaso
ning behavior after retrieval.

## Repository
 Layout

```text
.
├── .aaaSCRIPT/
│ 
  └── run_benchmark.sh
├── core/

│   ├── dataplane/
│   ├── da
emon/
│   └── local-suite/
├── 
deploy/
├── docs/
│   ├── asset
s/
│   │   ├── branding/
│   │ 
  │   ├── hms-banner.png
│   │   
│   ├── hms-hero.png
│   │   │ 
  ├── shadowweave-mark.png
│   │   
│   └── shadowweave_v6.png
│   │ 
  ├── benchmark_case_replay.svg
│   �
��   └── memory_pipeline_demo.svg
│  
 ├── benchmark_case_replay.html
│   �
��── memory_pipeline_demo.html
├── 
interface/
├── lab/
│   └── eva
luation/
│       └── benchmarks/
│ 
          ├── common/
│           │
   └── benchmark_runner.py
│         
  └── longmemeval/
│               �
�── longmemeval_benchmark.py
├── to
oling/
├── .env.example
├── READM
E.md
└── README.zh-CN.md
```

Important
 files:

- `.aaaSCRIPT/run_benchmark.sh`: uni
fied experiment script
- `scripts/run_memory_
demo.sh`: one-command automatic retain/recall
 demo
- `examples/automatic_memory/openai_res
ponses.py`: two-turn OpenAI Responses API exa
mple
- `docs/assets/branding/hms-banner.png`:
 project identity banner
- `docs/assets/brand
ing/hms-hero.png`: compact README project hea
der
- `docs/assets/branding/shadowweave-mark.
png`: compact ShadowWeave team mark
- `docs/a
ssets/branding/shadowweave_v6.png`: ShadowWea
ve team identity artwork
- `docs/benchmark_ca
se_replay.html`: auto-playing single-case pro
cess replay
- `docs/assets/benchmark_case_rep
lay.svg`: README-embedded animated case repla
y
- `docs/memory_pipeline_demo.html`: static 
before/after visualization
- `docs/assets/mem
ory_pipeline_demo.svg`: README-embedded visua
l summary
- `lab/evaluation/benchmarks/longme
meval/longmemeval_benchmark.py`: LongMemEval 
pipeline implementation
- `lab/evaluation/ben
chmarks/common/benchmark_runner.py`: shared e
valuation runner
- `.env.example`: local conf
iguration template

## Environment Setup

Cre
ate a local environment file:

```bash
cp .en
v.example .env
```

Open `.env` and replace t
he `*_change_me` values. The main model setti
ngs are:

| Pipeline role | Base URL | API ke
y | Model |
| --- | --- | --- | --- |
| Core 
HMS / recall organization | `HMS_API_LLM_BASE
_URL` | `HMS_API_LLM_API_KEY` | `HMS_API_LLM_
MODEL` |
| Retain / fact extraction | `HMS_AP
I_RETAIN_LLM_BASE_URL` | `HMS_API_RETAIN_LLM_
API_KEY` | `HMS_API_RETAIN_LLM_MODEL` |
| Ans
wer generation | `HMS_API_ANSWER_LLM_BASE_URL
` | `HMS_API_ANSWER_LLM_API_KEY` | `HMS_API_A
NSWER_LLM_MODEL` |
| LLM judge | `HMS_API_JUD
GE_LLM_BASE_URL` | `HMS_API_JUDGE_LLM_API_KEY
` | `HMS_API_JUDGE_LLM_MODEL` |
| Embeddings 
| `HMS_API_EMBEDDINGS_OPENAI_BASE_URL` | `HMS
_API_EMBEDDINGS_OPENAI_API_KEY` | `HMS_API_EM
BEDDINGS_OPENAI_MODEL` |

All roles may point
 to the same OpenAI-compatible service. In th
at case, use
the same Base URL and API key in
 each section while choosing models appropria
te
for each role. Also configure:

- `HMS_API
_DATABASE_URL`: a reachable PostgreSQL databa
se with `pgvector`
- `HMS_DATASET_PATH`: the 
local LongMemEval dataset JSON path
- `HMS_PI
PELINE`: `ledger` or `self_evolution`

The fr
amework loads configuration from `.env`. Do n
ot hard-code credentials in
the source code, 
and never commit the populated `.env` file.


## Reproduction Logic

The benchmark script n
ow defaults to the full clean reproduction pa
th:

```text
Retain -> Recall -> Answer -> Ju
dge
```

For every benchmark item, HMS first 
retains the conversation sessions, recalls
re
levant memories for each question, generates 
a grounded answer, and finally
uses the confi
gured judge model to score that answer agains
t the gold answer.

Recommended first run:

`
``text
1. Copy .env.example to .env
2. Fill d
atabase, Base URL, API key, model, and datase
t settings
3. Start with one or two benchmark
 instances
4. Verify Retain, Recall, Answer, 
and Judge all complete
5. Increase concurrenc
y and benchmark size
6. Inspect results under
 .aaaRESULT/ and logs under .aaaLOG/
```

Use
 `HMS_RETRIEVAL_ONLY=1` only for a later iter
ation when the same memories are
already pres
ent in the database and you intentionally wan
t to rerun only
Recall → Answer → Judge.


## Minimal End-to-End Run

```bash
cp .env.e
xample .env
# Edit .env before continuing.

e
xport HMS_BENCHMARK=longmemeval
export HMS_PI
PELINE=ledger
export HMS_RETRIEVAL_ONLY=0
exp
ort HMS_MAX_INSTANCES=2

bash .aaaSCRIPT/run_
benchmark.sh \
  --parallel 1 \
  --max-concu
rrent-questions 1 \
  --eval-semaphore-size 1

```

The script prints the active mode at st
artup. For a clean reproduction it must
print
 `HMS reproduction mode: Retain -> Recall -> 
Judge`.

## Run the Ledger Pipeline

```bash

export HMS_RETRIEVAL_ONLY=0
export HMS_PIPELI
NE=ledger
export HMS_MAX_INSTANCES=500
export
 HMS_SESSION_EXPANSION_WEIGHT=0.5

bash .aaaS
CRIPT/run_benchmark.sh \
  --parallel 8 \
  -
-max-concurrent-questions 8 \
  --eval-semaph
ore-size 8 \
  --quiet
```

## Run the Self-E
volution Pipeline

```bash
export HMS_RETRIEV
AL_ONLY=0
export HMS_PIPELINE=self_evolution

export HMS_MAX_INSTANCES=500
export HMS_SESSI
ON_EXPANSION_WEIGHT=0.5

bash .aaaSCRIPT/run_
benchmark.sh \
  --parallel 8 \
  --max-concu
rrent-questions 8 \
  --eval-semaphore-size 8
 \
  --quiet
```

## Common Runtime Options


Useful environment variables:

- `HMS_PIPELIN
E`: `ledger` or `self_evolution`
- `HMS_RETRI
EVAL_ONLY`: defaults to `0`; set to `1` only 
to reuse retained memories
- `HMS_MAX_INSTANC
ES`: limit the number of evaluated questions

- `HMS_MAX_QUESTIONS`: limit questions after 
filtering
- `HMS_DATASET_PATH`: provide a loc
al LongMemEval dataset path
- `HMS_SESSION_EX
PANSION_WEIGHT`: override session expansion w
eight
- `HMS_PYTHON_BIN`: use a specific Pyth
on interpreter

Useful command-line options:


- `--parallel`: number of instances processe
d concurrently
- `--max-concurrent-questions`
: maximum concurrent question-level tasks
- `
--eval-semaphore-size`: evaluator concurrency
 limit
- `--category`: run a specific LongMem
Eval category
- `--question-id`: run one or m
ore question IDs
- `--skip-ingestion`: skip i
ngestion and use existing database memories
-
 `--quiet`: reduce console output

## Runtime
 Artifacts

When the experiment runs, local r
untime artifacts are written under ignored
di
rectories:

```text
.aaaLOG/
.aaaRESULT/
```


These directories are for local reproduction
 and should not be committed.


