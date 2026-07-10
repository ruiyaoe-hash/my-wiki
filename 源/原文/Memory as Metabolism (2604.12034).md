---
source_url: https://arxiv.org/abs/2604.12034
source: arXiv 2604.12034
type: raw
created: 2026-07-06
tags: [学术论文, Agent记忆, raw]
---

# Memory as Metabolism (2604.12034)

> 原始来源: https://arxiv.org/abs/2604.12034
> 入库日期: 2026-07-06
> 提取方式: ar5iv HTML → 纯文本提取

Memory as Metabolism 

 A Design for Companion Knowledge
Systems 

 Stefan Miteski CODE University Berlin
stefan.miteski@ext.code.berlin 

 April 2026 (v3.642) 

 This paper was developed with AI-assisted research and editing
support. The author takes full responsibility for all claims, framing,
citations, and conclusions. 

 Abstract 

 Retrieval-Augmented Generation is still the dominant pattern for giving
LLMs persistent memory, but a visible cluster of personal wiki-style
memory architectures emerged in April 2026 — design proposals from
Karpathy, MemPalace, and LLM Wiki v2 that compile knowledge into an
interlinked artifact for long-term use by a single user, instead of
retrieving from raw documents on every query. They sit alongside
production memory systems that the major labs have been shipping for
over a year, and an active academic lineage including MemGPT, Generative
Agents, Mem0, Zep, A-Mem, MemMachine, SleepGate, and Second Me. Within a
2026 landscape of emerging governance frameworks for agent context and
memory — including Context Cartography ([45]) and MemOS ([24])
— this paper proposes a companion-specific governance profile: a set
of normative obligations, a time-structured procedural rule, and
testable conformance invariants for the specific failure mode of
entrenchment under user-coupled drift in single-user knowledge wikis
built on the LLM wiki pattern [20]. This is an interpretive reading
of the field, not a settled diagnosis — public docs may understate
internal theory, and the systems below were built for a range of
overlapping but distinct purposes. This paper contributes the design
language we found missing in our own reading. 

 The framework’s three layers — interaction/workflow (collect,
annotate, organize, revisit), representation/retrieval (storage format,
object types, retrieval index), and retention/governance (decay,
gravity, consolidation, audit) — are explicitly scoped: this paper is
primarily a theory of the third, with implications for the second
through the CONTEXTUALIZE operation. 

 Start with how the wiki decides what to keep. Recency and access
frequency are not enough. An entry should also earn its place by being
structurally load-bearing for the rest of the wiki, and by the user
actually getting useful results when the system acts on it. Pure recency
retains popular noise; pure access frequency punishes quiet foundations;
pure utility creates a satisfaction-chasing echo chamber. You need all
three, weighted against each other, plus a defense against any one
signal dominating. 

 That defense is memory gravity. Some entries are referenced by many
others; removing them fragments the wiki and orphans downstream
knowledge. A naive pruner — even a smart outcome-weighted one — will
eventually delete the foundations while retaining what was popular last
week. Memory gravity protects entries whose removal would cascade, the
same way architectural gravity protects load-bearing decisions in
software systems. It is dependency centrality applied to memory
retention, and it is what keeps the wiki from optimizing itself into
fragility. 

 Then the hard question: what happens when new information arrives that
contradicts what is already in the wiki? Karpathy’s lint operation
handles some of this reactively. Our proposal handles it the way humans
actually do — not at ingestion, but later, during a dedicated
integration pass modeled on sleep consolidation. New entries land in a
raw buffer. A shallow filter rejects obvious garbage at ingestion but
does not make coherence decisions. The real coherence work runs on a
schedule (nightly, weekly, whatever fits), and it scores entries against
each other as well as against the active wiki. This matters because a
single contradictory entry scored alone gets quarantined, but three
mutually-supporting entries arriving in the same buffer window can
accumulate enough pressure to challenge a high-gravity dominant
interpretation. Minority positions get a structural path to becoming
majority positions when the evidence justifies it, instead of being
silently routed to quarantine one by one. 

 This connects directly to the Kuhn problem [21]. Wikis ossify. Over
time the dominant interpretation gets more protected, newer
contradicting evidence gets more easily dismissed, and what started as a
living knowledge base turns into a paradigm maintenance system —
coherence preserved within the existing structure until anomalies
accumulate enough to force a shift. Normal science, not revolution. We
attack this with a periodic AUDIT operation that stress-tests the
highest-gravity entries — temporarily suspends them, reruns queries
that used to access them, and measures whether query performance
actually degrades. If the entry turns out to be dead weight, its gravity
decays. If removing it improved query performance, it was actively
interfering and gets archived. AUDIT is the framework’s main defense
against dogma, and we are honest that its sensitivity is an open
problem. 

 Underneath all of this is a design principle we think is missing from
current personal LLM memory discussions. Personal memory is a
 companion system — its job is to serve one user over the long
haul, not to track objective truth. That changes the design target in
specific ways: the system should mirror its user on operational
dimensions (working vocabulary, load-bearing structure, continuity of
context) and compensate on epistemic failure modes (entrenchment,
suppression of contradicting evidence, the Kuhnian ossification
described above). Mirror-vs-compensate is not a slogan; it is a decision
rule with a temporal structure. The streaming path preserves usability
in the moment. The scheduled consolidation and audit operations
adjudicate revision. 

 One architectural commitment worth flagging up front: the wiki stays
outside the base model weights. This is deliberate. It preserves a
correction channel the framework does not implement and does not need to
— when the base LLM gets updated by its lab (new factual priors, new
alignment training, new capabilities), the companion system inherits
those updates for free because swapping the model is a configuration
change, not a wiki operation. A user running this for five years is not
running the same reasoning engine at year five, even if the wiki looks
identical. Fold the wiki into weights and you lose this channel. 

 Finally, the scope question. Everything above concerns single-agent
systems. The interesting follow-on problems live at the federation level
— family wikis, team wikis, department wikis, community wikis — each
of which has different update dynamics (generational turnover,
onboarding, role handoffs, membership churn). Federation is a distinct
research direction, not a rescue for what single-agent systems cannot
do, and we name it as where the next layer of work belongs. 

 Honest scoping: the mechanisms are mostly borrowed from cognitive
architectures, recommender-system diversity, and graph centrality. The
contribution is how they are coordinated around a specific design rule
for a specific class of system. And honest safety: at the single-agent
level, the framework offers a partial story. It can resist entrenchment
and amplify genuine minority evidence. It does not eliminate the
reinforcement of user-held bad beliefs, and we do not pretend it does.
What we offer is an architecture that makes the gap visible, names three
correction channels that attack it on different timescales, and points
at the specific directions where the remaining work lives. 

 The safety story is explicitly partial: the framework offers structural
defenses on three timescales — scheduled within-agent consolidation
cycles, cross-agent federation, and base-model evolution — but does
not solve the reinforcement-of-bad-beliefs problem and does not claim
to. 

 1. Introduction 

 1.1 Three claims, separately
defended 

 Much of the difficulty in current LLM memory literature comes from
conflating three distinct claims. We separate them. 

 The descriptive claim. Personal LLM memory systems built around
incremental wiki compilation already exhibit user-coupled retention
dynamics that can accumulate into drift over time. Karpathy’s LLM Wiki
[20] grows by integrating what the user finds worth integrating.
MemPalace [17] retains what the user’s usage patterns reinforce. LLM
Wiki v2 [11] decays what the user does not return to. None of these
systems is a neutral knowledge infrastructure. Each is position-ful and
personalized, even when its documentation does not say so. 

 The taxonomic claim. This drift is sufficient grounds to
specify the retention-governance obligations that follow from treating
personal single-user LLM memory as a distinct design class — a class
that prior work has named without governing. Human-centered computing,
user modeling, adaptive interfaces, and personal knowledge management
have long drawn similar distinctions between systems that serve a
specific user’s goals and systems that serve a general information need.
We are not the first to draw this line. MemoryBank (arXiv:2305.10250)
already uses “long-term AI Companion scenario” as a primary capability
descriptor. Second Me (arXiv:2503.08102) explicitly frames single-user
memory as a “memory offload system” serving one user. LongMemEval
(arXiv:2410.10813) ties long-term memory evaluation to contexts
including “psychological counseling or secretarial duties.” Recent
surveys (spanning 2024–2026) treat “personalized” as an established
memory category ([13]; [44]; [51]). What is missing is not
the word companion but a normative specification of what
retention-governance obligations follow from treating a system as one
— what it must mirror, what it must compensate for, what separability
requires, and why those obligations make the class designable in ways
that “personalized” or “companion-scenario” alone do not. That
specification is what this paper provides. 

 The normative claim. Given the descriptive fact and the
taxonomic distinction, the retention policy for companion memory should
follow a specific design principle we introduce in Section 1.2 —
mirror on operational dimensions, compensate on epistemic failure modes.
This is where the contribution lives. The descriptive claim is
observation; the taxonomic claim is a classification move others have
made in adjacent domains; the normative claim is the design rule we
propose and defend. 

 Each claim stands alone. The taxonomic claim does not depend on agreeing
with the normative one. The normative claim does not assume the
descriptive claim is settled — it gives a design rule that remains
useful even if reasonable people disagree about whether current systems
already drift. 

 1.2 Mirror where mirroring serves utility. Compensate
where mirroring damages
it. 

 A companion system should mirror its user on some dimensions and
compensate for its user on others. The selection rule is instrumental,
not philosophical. 

 A companion system mirrors its user on operational dimensions:
the working context the user is currently reasoning within, the
load-bearing structure the user depends on for coherent thought, the
continuity of self-reference that lets the user pick up where they left
off, the vocabulary and framing the user has developed over time. On
these dimensions, alignment is the design goal and deviation is the
failure mode. A companion that refused to inherit its user’s vocabulary
would not be usable. 

 A companion system compensates for its user on epistemic failure 
dimensions: entrenchment of demonstrably false high-gravity entries,
suppression of evidence contradicting settled beliefs, convergence
toward monoculture under repeated use. On these dimensions, alignment is
the failure mode and deviation is the design goal. A companion that
inherited its user’s every confirmation bias would be harmful. 

 The mirror-vs-compensate vocabulary itself is not new. Qian et
al. (arXiv:2510.01924) uses it explicitly in “To Mask or to Mirror”
— empirically observing that some models mirror human biases while
others mask and compensate for them at inference time, and naming the
tension in terms close to this paper’s own. The sycophancy literature
frames over-mirroring as a failure mode requiring procedural mitigation.
The offline consolidation pattern that implements the compensate side is
also established: LightMem (arXiv:2510.18866) explicitly frames its
design as “sleep-time computation that decouples consolidation from
online inference,” and SleepGate (arXiv:2603.14517) proposes periodic
sleep micro-cycles for KV-cache consolidation. What neither the
vocabulary nor the individual mechanisms provide is a
 time-structured procedural conflict rule for resolving the
mirror-vs-compensate tension in a personal companion-memory substrate
— specifically, a decision procedure governing what gets buffered
versus quarantined versus audited, across which timescale, and with what
decision consequences at each stage. The contribution is the TRIAGE →
CONSOLIDATE → AUDIT execution model as a binding: not the discovery of
the tension, and not the individual operations, but the procedural rule
that decides how and when each operation applies to the
mirror-vs-compensate conflict in a companion wiki. 

 The analogy is corrective rather than substitutive. A cane mirrors the
user’s gait — it does not try to walk differently. A cane does not
mirror a limp — it compensates for it. Glasses mirror the user’s
visual field and compensate for its distortion. Companion memory should
mirror operational continuity and compensate for epistemic entrenchment.
The framework’s five operations implement this split. TRIAGE, DECAY, and
memory gravity are mirror mechanisms. CONSOLIDATE, AUDIT, and
CONTEXTUALIZE are compensate mechanisms — CONTEXTUALIZE in a more
specific sense, addressed in Section 5.4 below: it compensates for the
assumption that external sources have a single canonical compression by
fitting them to the user’s working context depth at consolidation time. 

 The tension between mirror and compensate is not a bug to resolve. It is
the design principle. Any companion memory framework that claims to only
mirror is unsafe; any framework that claims to only compensate is not a
companion. 

 When mirror and compensate point in opposite directions, the framework
defaults to preserving operational continuity in the streaming path and
routing the conflict to scheduled compensate operations. A single
contradiction should not overwrite a high-gravity entry in real time —
that would destroy the continuity the companion is supposed to provide.
But coherence concerns should not be allowed to suppress accumulated
counterevidence indefinitely either. TRIAGE preserves usability in the
moment. CONSOLIDATE and AUDIT decide whether revision has earned
structural change. The rule is procedural rather than algorithmic:
mirror by default under time pressure, compensate during scheduled
integration windows, and treat AUDIT as the tiebreaker when a
gravity-protected entry is implicated in repeated bad outcomes across
multiple cycles. (See §5.0 for the conflict routing matrix that
instantiates this rule case-by-case.) 

 1.3 The circularity is the
thesis 

 A frequent objection to coherence-based memory policies is that they are
self-sealing: coherence is measured against the current wiki, which is
the product of past coherence decisions. Under a truth-tracking framing,
this would be a fatal flaw. Under the companion framing, it is what
having a stable self looks like rather than dissociating every time new
information arrives. We accept the circularity on the mirror side and
build the framework’s compensate side — batched consolidation and
audit — specifically to resist its failure modes without pretending to
escape it. 

 1.4 Contributions 

 1. 

 A triple-tracked framing of personal LLM memory — descriptive,
taxonomic, normative — that separates observation, classification,
and design rule rather than collapsing them. 

 2. 

 The mirror-vs-compensate design principle as an instrumental selection
rule for which user properties a companion system should inherit,
operationalized as a time-structured procedural conflict rule across
streaming, consolidation, and audit timescales. 

 3. 

 A five-operation retention policy (TRIAGE, CONTEXTUALIZE, DECAY,
CONSOLIDATE, AUDIT) built around a raw buffer and a batched
consolidation cycle modeled on sleep function. 

 4. 

 Two supporting mechanisms: memory gravity (load-bearing protection for
operational continuity) and minority-hypothesis retention (variance
against monoculture collapse). 

 5. 

 Four predictions with operational proxies: coherence stability,
fragility resistance, monoculture resistance, effective
minority-hypothesis influence — where influence is defined as
measurable change in downstream outputs, not mere storage or
surfacing. 

 6. 

 An honest safety story with three correction channels — within-agent
consolidation, cross-agent federation across named unit types, and
base model evolution preserved by architectural separability — and
explicit acknowledgment of what the framework does not solve. 

 We do not present implementation results. This is a vision paper
proposing a normative governance profile for a specific system class. 

 2. Background and Related
Work 

 2.1 LLM Memory Systems 

 A note on sources: this paper draws from peer-reviewed
publications, arXiv preprints, practitioner-published design documents
(including GitHub gists), and community-reported analyses of production
systems. These carry different evidential weight. Where a claim rests
primarily on community reporting rather than official documentation, the
text marks this explicitly. The community-reported characterizations of
production systems — particularly the Auto Dream mechanism attributed
to Anthropic — are included as motivating context for the design
framework, not as settled empirical claims. 

 The literature map below is interpretive and necessarily incomplete; it
maps the design space as the author reads it, not as a systematic review
would establish it. 

 Retrieval-Augmented Generation [23] treats every query as a fresh
retrieval problem — knowledge is indexed but never consolidated. Three
open projects proposed alternatives in April 2026: Karpathy’s LLM Wiki
[20] addresses the stateless-LLM problem by proposing that the model
should incrementally compile a persistent interlinked knowledge base as
it reads new sources; MemPalace (Jovovich & Sigman, 2026) adds a
hierarchical spatial retrieval architecture reporting 96.6% R@5 on
LongMemEval; LLM Wiki v2 [11] adds Ebbinghaus-inspired time decay
and consolidation tiers. Obsidian is Karpathy’s rendering surface; the
graph structure follows from interlinking rather than being the design
goal. 

 Karpathy’s LLM Wiki is the clearest open substrate this paper
directly governs. Karpathy identifies three architectural layers —
raw sources (immutable input), the compiled wiki (LLM-maintained
markdown files), and the schema (the configuration document telling the
LLM how the wiki is structured and what workflows to follow). He notes
that “the wiki is just a git repo of markdown files” and explicitly
leaves the schema “intentionally abstract,” designed to be co-evolved
between the user and the LLM for each domain. The companion governance
profile proposed in this paper is a governed instantiation of that
schema: normative obligations, vitality mechanics, and structural audit
cycles that Karpathy left to each user to instantiate. His pattern
identifies the substrate; this paper specifies the obligation-level
rules that should govern it for companion memory specifically. The
integration with existing systems is additive: Karpathy’s LLM Wiki
provides the incremental compilation pattern; the companion layer adds a
raw buffer tier, a scheduled consolidation cycle, and metadata
structures for gravity and cohesion tracking. 

 LLM Wiki v2 [11] extends Karpathy’s base pattern with
explicit lifecycle governance proposals: Ebbinghaus-inspired retention
curves, multi-tier consolidation (working/episodic/semantic/procedural),
schedule-driven maintenance, and audit trail recommendations. This is
the closest practitioner-level prior art to the governance profile this
paper proposes, and the delta must be stated explicitly. LLM Wiki v2
proposes these mechanisms informally as implementation patterns without
normative obligations — it does not specify what a companion wiki MUST
do, what it MUST NOT do, or what failure looks like for the specific
entrenchment failure mode. This paper adds three things LLM Wiki v2 does
not provide: (1) explicit entrenchment stress-testing via
AUDIT-by-suspension tied to utility traces; (2) explicit minority
retention across cycles against centrality-protected incumbents, with
multi-cycle buffer pressure as the integration mechanism; and (3)
companion-specific normative obligations that distinguish what should be
mirrored from what should be compensated, and why. 

 These projects are not the whole state of the art. Much of the relevant
frontier lives in production at the major LLM labs and in an active
academic literature, and both have been working on LLM memory for over a
year with substantial deployment data. A proper engagement with prior
work has to credit them honestly. The reading of these systems
below is interpretive rather than exhaustive; the point is to locate
common architectural tendencies, not to provide definitive product
analysis. Some of these systems target overlapping but distinct
problems, and grouping them should not be read as a claim that they are
all solving the same task. 

 Anthropic (Claude Code). CLAUDE.md hierarchical memory with
scope-based instruction loading; per Anthropic’s documentation, more
specific contexts take precedence over broader ones, with project-level
instructions taking priority over user-level instructions in conflict
resolution. Auto Memory for session-level capture. A between-session
consolidation mechanism — referred to as “Auto Dream” in
community documentation and third-party analysis, though not named as
such in official Anthropic docs — is reported to perform contradiction
resolution, date normalization, stale-entry pruning, and overlap
merging, with the sleep/REM framing representing community
interpretation rather than Anthropic’s own characterization. Memory Tool
API with view/create/str_replace/insert/delete/rename primitives
(officially documented). If the community-reported consolidation
behavior is accurate, it is the closest shipping parallel to this
paper’s CONSOLIDATE operation. Anthropic ships mechanisms without
publishing design principles. 

 OpenAI (ChatGPT). Memory live since 2024, with Saved Memories
(explicit) and Reference Chat History (implicit) mechanisms. Community
analysis has proposed a four-layer architecture that is not RAG — no
vector database, no embedding similarity search (Khemani, 2025,
community reverse-engineering; not official OpenAI documentation).
User-visible inspection, edit, delete. ChatGPT Memory is configured
through ChatGPT settings and operates at the product layer; the OpenAI
Responses API separately supports stateful conversation interactions,
which are architecturally distinct from the ChatGPT memory features. 

 Google (Gemini / NotebookLM). Gemini 3 Pro has a 1M token
context window. Google’s strategy is effectively context-window
expansion as a partial substitute for sophisticated memory architecture
— if you can fit everything in context, the forgetting problem is
deferred rather than solved. This is architecturally opposite to the
framework we propose, and worth engaging as an alternative design
philosophy. 

 DeepSeek-OCR (Wei, Sun, Li, arXiv 2510.18234, October 2025). An
open-source proposal to implement forgetting via progressive visual
compression. Long contexts are rendered as images, and older content is
progressively resized to smaller, blurrier images over time. 10x
compression holds at ~97% OCR accuracy, 20x holds at
~60%. The paper frames this as a “memory forgetting
mechanism in LLMs” and draws the biological analogy explicitly —
recent memories stay sharp, old memories fade. DeepSeek-OCR operates at
a different architectural layer than our framework: it proposes a
 mechanism for graceful forgetting, we propose a design
language for retention decisions such mechanisms implement. The two
compose rather than compete. Subsequent work has contested the specific
mechanism — Context Cascade Compression (C3, arXiv 2511.15244)
achieves 93% at 40x via cascading two LLMs, and an adversarial critique
(arXiv 2512.03643) argues simple mean pooling outperforms the optical
approach at matched budgets — which demonstrates that the mechanism
space for LLM forgetting is actively contested. 

 Academic lineage — Generative Agents and MemGPT. Park et
al. (arXiv 2304.03442, UIST 2023) introduced the “memory stream” — a
comprehensive raw record of all agent experiences — combined with
periodic “reflection” synthesis into higher-level abstractions. This
is a clear structural precursor to the pattern this paper builds on: a
TRIAGE-filtered raw capture feeding a buffer that a scheduled
CONSOLIDATE operation processes into a longer-term store. Generative
Agents is highly cited and must be acknowledged directly: the
buffer-plus-reflection pattern is prior art at the mechanism level. What
the companion framework adds is a normative design rule governing
 which retention decisions are right within that pattern, and a
named correction channel through architectural separability. Packer et
al. (MemGPT, arXiv 2310.08560, 2023) then formalized LLM memory as
 virtual context management borrowed from operating-system virtual
memory paging: the LLM manages what sits in its own context window via
function calls, moving data between main context and external archival
storage. MemGPT explicitly names “virtual companions or personalized
assistants” as the use case where context budgets run out quickly,
which is the same class of system this paper theorizes. MemGPT’s
architecture is silent on which retention decisions are right —
it provides the machinery for moving data between tiers without a design
language for deciding what belongs in which tier. 

 Second Me (arXiv 2503.08102). An intelligent, persistent memory
offload system that retains user-specific knowledge across contexts for
a single user. In this paper’s taxonomy — not a claim Second Me makes
about itself — it is among the closest existing system-level neighbors
to the companion-memory design class this paper names. The distinction
is normative rather than architectural: Second Me describes the class
behavior and builds a working system; this paper provides the evaluation
target and the retention-policy obligations that should govern such
systems. Second Me does not specify what the system must mirror, what it
must compensate for, or what separability requires — the normative
specification is what is absent, and that absence is what this paper
fills. 

 Successor systems and the sleep-consolidation pattern. 
SleepGate (arXiv 2603.14517) proposes “sleep micro-cycles” over the
KV-cache with a forgetting gate and consolidation module, triggered
periodically. This complements LightMem (arXiv:2510.18866), which frames
its offline consolidation as “sleep-time computation that decouples
consolidation from online inference.” Taken together, SleepGate,
LightMem, and the community-reported Auto Dream mechanism suggest that
the sleep-consolidation pattern is emerging independently across
multiple architectural layers — KV-cache, external wiki, and
companion-memory retention policy. The design vocabulary for why it
belongs specifically in companion-memory systems is what is missing.
Mem0 (Chhikara et al., arXiv 2504.19413, April 2025) is the strongest
documented production-paper in this lineage, proposing dynamic
extraction, consolidation, and retrieval of salient information from
ongoing conversations with a graph variant for relational structures,
and reporting a 26% improvement over OpenAI on LLM-as-a-Judge on the
LOCOMO benchmark plus 91% lower p95 latency and 90%+ token cost
savings; Zep uses a temporal knowledge graph with time-aware validity
windows (Zep / Graphiti, arXiv 2501.13956); A-Mem (arXiv 2502.12110)
reports an 85-93% token reduction versus MemGPT via interconnected
atomic notes; MemMachine (arXiv 2604.04853, March 2026) explicitly
grounds its design in Tulving’s episodic/semantic distinction and
critiques the MemGPT lineage for “accuracy concerns from probabilistic
extraction and compounding error over time.” MemMachine’s critique is
essentially the fragility-under-drift problem this paper’s CONSOLIDATE
operation addresses — the academic community is converging on the same
failure mode we are, at roughly the same time, and trying to solve it at
the mechanism layer. 

 MemOS ([24]) is the closest prior art to the
retention/governance layer this paper proposes and must be engaged
directly. MemOS explicitly names “Memory Governance” as a design stage
with access control, versioning, and provenance auditing. It uses an
L0/L1/L2 tiering structure — raw (L0), structured (L1), and
internalized preferences (L2) — that maps structurally onto the cold
memory / raw buffer / active wiki architecture proposed here. MemOS
frames governance as a safety foundation, which aligns with the
companion framework’s treatment of AUDIT and minority-hypothesis
retention as safety mechanisms rather than optional optimizations. The
distinction is normative rather than architectural: MemOS describes
governance as an engineering architecture; this paper specifies the
obligation-level rules that should govern it for companion systems
specifically — what the system must mirror, what it must compensate
for, and why those obligations make the governance rules non-optional
for this class. MemOS does not specify what a companion wiki must retain
as a function of epistemic drift, what it must compensate for as a
function of entrenchment, or why separability is a safety commitment
with a named rationale. The normative specification is what the
companion framework adds to the governance architecture MemOS names. 

 The harness engineering review ([53]) explicitly recommends
cross-model transfer tests for memory systems and argues that
reliability gains come from changing the environment around the base
model rather than the model itself — directly encroaching on the
separability contribution. The companion framework’s response is in
Section 8.3: the paper’s separability claim is not that external memory
is more reliable (the harness review’s framing) but that separability
specifically preserves the base-model evolution correction channel
against user-coupled epistemic entrenchment. That rationale is narrower
and more specific than the harness review’s argument, and it remains
intact. 

 Context Cartography ([45], March 2026) is the closest
competitor at the governance-layer level and must be engaged directly.
It proposes a formal framework for the deliberate governance of
contextual space with seven cartographic operators, explicit state
transitions, failure mode classification, and a diagnostic benchmark
designed for operator ablation — parts of which are mechanically
verified in Lean 4. This occupies the governance-layer slot this paper
also targets, and the distinction must be stated precisely. Context
Cartography governs contextual space as a general problem: zones,
operators, generalization across agent types. This paper governs a
specific failure mode in a specific system class: entrenchment under
user-coupled drift in single-user companion wikis. The contribution is
not the existence of a governance layer — Context Cartography and
MemOS both provide governance layers — but a companion-specific
normative profile: what a single-user wiki MUST do when faced with the
specific failure mode of coherence-preserving drift that gradually
protects dominant interpretations against legitimate revision. The
evaluation target also differs: Context Cartography evaluates via
operator ablation; this paper’s sharpest prediction targets multi-cycle
buffer pressure accumulation under centrality-protected entrenchment,
which no existing operator ablation scheme captures. 

 What all of this means for this paper’s contribution. 
Mechanism-level parallels are substantial and honest engagement requires
acknowledging them. At least six mechanisms in our framework have direct
parallels in shipped or published work: consequence-weighted retention
(OpenAI, Anthropic), batched consolidation (Anthropic,
community-reported; Generative Agents, 2023), hierarchical memory with
scope-based precedence tiers (Anthropic CLAUDE.md), contradiction
resolution during integration (Anthropic, community-reported),
stale-entry pruning (Anthropic, community-reported), user-managed
forgetting (OpenAI, Anthropic). The framework we propose is not a claim
to have invented the mechanisms. It is a claim to provide design
vocabulary the field has not assembled in this form — a named system
class with normative obligations , a principled retention policy
for that class, and an honest scope of what such systems can and cannot
do. Section 8.2 engages this more fully. 

 The intent taxonomy gap. The field now has at least six major
survey papers (2024–2026) and they are genuine contributions. The AI
Hippocampus (Jia et al., arXiv 2601.09113, TMLR 2025) organizes LLM
memory into implicit/explicit/agentic paradigms by representational
substrate. [13] uses forms/functions/dynamics. [44] uses
object/form/time. [51] uses sources/forms/operations. None of these
is a companion-memory taxonomy. All are mechanism taxonomies — they
distinguish systems by how they work, not by what they are
for . What existing taxonomies do not provide is an intent
taxonomy : an account of which evaluation target and which design
obligations distinguish one system class from another. A companion
memory system and a memory platform may share identical architectural
mechanisms but differ in what success looks like and what
retention-policy obligations follow. The AI Hippocampus’s
implicit/explicit/agentic axis is orthogonal to this paper’s
companion-memory class; citing it here is not a concession but a
demonstration that the field’s best surveys are organized by substrate
while the design-class distinction this paper draws operates on a
different axis entirely. The intent taxonomy is what this paper names. 

 2.2 User-Aligned System Design as Prior
Art 

 The distinction between systems built to serve a specific user and
systems built to serve general information needs is not new to this
paper. Human-centered computing has developed it across decades of
adaptive interface, user modeling, and personalization research.
Personal knowledge management (PKM) treats individual knowledge bases as
artifacts whose value is measured by personal utility rather than
objective completeness. Communities of practice literature addresses how
small groups maintain shared knowledge that serves the group without
claiming general validity. We inherit the distinction from these
traditions and apply it to LLM memory, where it has not been drawn
cleanly in current discussions. 

 Wikipedia’s governance architecture is a structurally instructive
parallel for the CONSOLIDATE and AUDIT operations, worth noting before
those operations are specified in Section 5. Wikipedia maintains
coherence at civilizational scale through a multi-agent governance
model: a large population of editors contribute changes to a shared
knowledge base, while a structured system of talk pages, revision
history, and flagged revisions adjudicates disputes and contested
claims. The talk page process is structurally analogous to CONSOLIDATE
— contested claims are scored against existing content, minority
positions are preserved and visible rather than silently overwritten,
and integration decisions emerge through a deliberation process. The
featured article and good article review processes are structurally
analogous to AUDIT — high-prominence articles are periodically
stress-tested by reviewers who temporarily impose additional scrutiny to
confirm their quality remains load-bearing. Two key differences mark the
companion framework as distinct: Wikipedia’s governance is multi-agent
and human-operated, while the companion framework’s governance is
single-agent and automated. These differences are design features, not
limitations — the companion framework achieves faster consolidation
cycles precisely because it does not wait for human editorial consensus,
and its single-user scope makes the multi-agent coordination problem
unnecessary. The Wikipedia parallel is useful as a template for the
governance logic, not as a claim that the two systems are equivalent in
scope or mechanism. 

 A second important lineage comes from formal belief revision and truth
maintenance systems in knowledge representation. In the AGM framework
and related work on epistemic entrenchment (Gärdenfors & Makinson,
1988), revision policies rely on an ordering over beliefs that
determines retraction priority when new information creates
inconsistency. Memory gravity functions as a pragmatic, graph-based
proxy for this kind of entrenchment ordering: it protects structurally
load-bearing entries based on downstream fragmentation cost rather than
purely logical postulates — and the key difference is that gravity is
prospective (what would break if this entry were removed now) rather
than retrospective (what has historically referenced it). 

 Complementing this, Truth Maintenance Systems [6] maintain explicit
dependency networks and justifications, allowing selective retraction
while preserving consistent alternatives. The minority-hypothesis
retention and branch mechanism proposed here draws structural
inspiration from TMS-style dependency-directed revision, but adapts it
to an LLM-compiled wiki substrate: alternatives are kept alive across
scheduled consolidation cycles rather than under immediate logical
revision, and promotion decisions are driven by accumulated pragmatic
utility and multi-cycle buffer pressure rather than symbolic consistency
alone. These traditions therefore inform the governance profile
developed in Section 5, while the companion-specific normative
obligations — mirror operational continuity while compensating
epistemic failure under user-coupled drift — remain the distinguishing
contribution of this framework. 

 2.3 Individual Memory Models and Sleep
Consolidation 

 ACT-R’s base-level learning [1] models memory activation as a
function of use history. Ebbinghaus’s forgetting curve [7] grounds
spaced repetition. Tulving’s episodic/semantic distinction [40] maps
onto the raw buffer and active wiki tiers in our framework. 

 More directly relevant to Section 5 is the cognitive neuroscience
literature on sleep consolidation. Tononi’s synaptic homeostasis
hypothesis and McClelland’s complementary learning systems both describe
the same basic pattern: episodic experience accumulates in a
fast-learning buffer during waking hours, and the deep integration work
— coherence checking, contradiction resolution, transfer to long-term
stable structure — happens offline during sleep. This is more than a
decorative analogy. It provides an architectural template for how
bounded agents can separate rapid capture from slower
coherence-preserving integration, and our framework implements the same
pattern at the architectural level without claiming the
neuroscience-to-system mapping is mechanistically exact. 

 A third precedent worth flagging — though we treat it as future-work
direction rather than as an established building block — is the
tiered-coherence pattern found in mature legal systems. European civil
law systems maintain coherence at civilization scale by layering
knowledge with different update frequencies and procedural protections:
constitutional principles that change across generations, primary
legislation that changes across decades, secondary regulation that
changes across years, and case law that updates continuously. This
shares structural features with the design problem the companion memory
framework addresses, though the legal solution rests on legitimacy,
authority, and institutional process — not just coherence management.
The framework’s gravity model implicitly points in a similar direction,
and a natural extension worth exploring would formalize gravity as a
discrete tier structure with different procedural protections per tier.
One honest caveat: the legal-system precedent does not promise
determinism. The same text — for example Council Regulation (EEC)
3720/85 — has produced materially different implementations across
member states, because legal application has interpretive latitude the
text does not eliminate. The same is true for companion memory wiki
content read by an LLM. Fixed text yields bounded variation in
downstream behavior, not a single deterministic output. The framework
should be read as constraining the range of LLM interpretation rather
than collapsing it; this is a structural property of the architecture,
not a bug to fix. A proper engagement with legal scholarship on tiered
coherence — Hart’s primary/secondary rules, Luhmann’s
systems-theoretic treatment of law, comparative constitutional design
— is reserved for future work. 

 2.4 Pragmatism and the Re-entry of Truth Through
Consequences 

 Consequence-weighted retention has serious philosophical precedent. The
pragmatist tradition — Peirce, James, Dewey — treats beliefs as
tools for action whose value is measured by practical consequences
rather than correspondence with an external reality the agent cannot
directly access. 

 This does not exempt companion systems from truth concerns. It reroutes
them. Under pragmatism, false beliefs become problematic when they
produce failed actions — damaged plans, broken relationships, health
harms, safety failures. Truth objections do not disappear; they come
back through consequences. The framework’s utility signal is the channel
for this re-entry. A retained entry that consistently produces bad
outcomes loses its retention whether or not anyone has labeled it
 false . Pragmatism lets the framework sidestep correspondence as a
design target while keeping consequence tracking as a correction
mechanism. 

 The apparent tension between “not a truth-tracker” and “uses
consequence as a retention signal” resolves under pragmatism. The
framework does not measure correspondence with external reality — it
has no truth oracle. What it measures is pragmatic fitness: did acting
on this entry produce outcomes the user judged useful? Did its presence
improve or degrade subsequent task performance? Truth re-enters through
consequence, not through correspondence. A false entry that consistently
produces failed actions loses its vitality through the utility signal. A
false entry that happens to produce successful actions in the short term
is harder to dislodge — but that is not a design flaw, it is the
correct characterization of how human memory actually works. The
framework makes this dynamic visible and auditable rather than
pretending to escape it. 

 3. The Accumulation Problem,
Reframed 

 Storage cost, retrieval latency, and relevance noise are real
consequences of accumulation-only memory. Under some retrieval
architectures, larger corpora may degrade retrieval quality; under
better-indexed architectures, they may not. We do not treat this as the
primary motivation for the framework. 

 The primary motivation is that personal LLM memory systems are
personalizing retention in ways that can accumulate into drift, whether
or not their designers name the dynamic (descriptive claim, Section
1.1), and the design question is not “how do we prevent drift” but
“how do we mirror productively and compensate intelligently while the
drift happens.” Naming the class is the precondition for giving it a
retention policy that serves its actual purpose rather than a policy
that pretends to serve a larger one. The operations that implement this
policy are specified in Section 5; before those operations can be
precisely defined, Section 4 names the objects they act on. 

 4. System Model 

 Before specifying operations, the framework names the objects those
operations act on and the states each object can occupy. This is the
system’s object model — analogous to RDF’s abstract syntax or the data
model sections in Spanner and Dynamo. Every operation in Section 5 reads
from and writes to one or more of these entities. Naming them explicitly
is what allows conformance to be tested: if an implementation uses
different object boundaries or drops a required state transition, it is
not implementing this framework. 

 Core entities 

 Entity 

 Lifecycle states 

 Status flags 

 Required fields 

 Raw buffer entry 

 pending → consolidated / rejected / expired 

 — 

 stable ID (content hash), ingestion timestamp, source pointer (Git blob
hash), origin channel, initial priority, candidate edge placeholders 

 Active wiki entry 

 active → decaying → archived 

 gravity-protected
(set by DECAY/AUDIT; orthogonal to lifecycle); quarantined (set by
CONSOLIDATE for low-cohesion entries; orthogonal to lifecycle) 

 ID,
commit hash, vitality score, gravity weight, quarantine flag,
last-accessed timestamp, cohesion bucket 

 Cold memory object 

 stored → recalled → re-compressed 

 — 

 ID, Git
blob hash, original source URL or path, linkout commitment flag
(non-optional) 

 Audit record 

 created → closed 

 — 

 entry ID, timestamp, suspension
result (degraded / unchanged / improved), outcome (restored /
gravity-reduced / archived) 

 Minority branch 

 open → promoted → closed 

 — 

 Git branch reference,
incumbent entry ID, cluster size, contradiction edge count, cycles
open 

 Note: gravity-protected and quarantined are
status flags, not lifecycle stages. An entry can be active and
 gravity-protected simultaneously. An entry can be
 decaying and quarantined simultaneously. This matters
for conformance: conformance invariants that reference these flags apply
regardless of the entry’s current lifecycle stage. 

 State transition rules 

 Raw buffer entries are created by TRIAGE and consumed by CONSOLIDATE.
They do not transition backwards — an entry either gets consolidated,
rejected on content grounds, or expires after the TTL window. Content is
immutable from the moment TRIAGE commits the entry. An entry in
 pending state MUST be readable by CONSOLIDATE without
modification. 

 Active wiki entries are created by CONSOLIDATE and modified by DECAY and
AUDIT. They are never deleted. The archived state is terminal:
full content moves to cold memory, the index record remains with a
tombstone flag. This preserves audit history and prevents silent data
loss. 

 Cold memory objects are created by CONTEXTUALIZE when it produces a
depth-fitted working representation of an external source. The original
is immutable. Re-compression creates a new cold memory object and
updates the active wiki entry’s commit hash — the prior cold memory
object is retained, not overwritten. 

 Minority branches are created by CONSOLIDATE when a cluster of
mutually-supporting entries fails individual integration but warrants
preservation. Branches close only via two explicit paths: promotion,
when the cluster crosses the promotion threshold during a CONSOLIDATE
cycle; or AUDIT-triggered archival, when AUDIT confirms the incumbent
entry remains load-bearing and the branch has not grown across a defined
number of cycles. Branches are never closed silently — if neither
condition has been explicitly evaluated and resolved, the branch remains
open. 

 Required invariants 

 • 

 Every active wiki entry MUST maintain a valid commit hash pointing to
its current content in Git 

 • 

 Every cold memory object MUST maintain a valid linkout to its original
source — this is the non-optional commitment CONTEXTUALIZE makes
when it processes an external source during scheduled consolidation 

 • 

 TRIAGE MUST assign a content hash as the stable ID before writing to
the buffer 

 • 

 Minority branches MUST NOT be closed silently — closure requires
either explicit promotion through CONSOLIDATE when the cluster crosses
the promotion threshold, or explicit AUDIT-triggered archival when
AUDIT confirms the incumbent remains load-bearing and the branch has
not grown across a defined number of cycles 

 • 

 Audit records MUST be append-only — no modification after creation 

 • 

 No operation MUST permanently delete any object — terminal states
are archived or expired , never hard-deleted 

 5. Companion Memory: The
Framework 

 5.0 Mapping operations to mirror and
compensate 

 Companion memory systems are analyzable across at least three layers.
The interaction/workflow layer handles collection, annotation,
organization, and revisitation — the territory of adaptive hypermedia
traditions that model and adapt to the individual user (Brusilovsky,
2001). The representation/retrieval layer handles how memory
exists as text, summaries, embeddings, and links, and how it is
retrieved — the territory of parametric and non-parametric memory
combinations in retrieval-augmented architectures [23]. The
 retention/governance layer determines what survives, how it is
protected, and when it is revised — closer to lifecycle control and
architectural fitness than to retrieval alone [9]. This paper
operates primarily at the retention/governance layer, with CONTEXTUALIZE
reaching into the representation/retrieval layer to determine the form
in which external sources enter the wiki. The interaction/workflow layer
is out of scope: a companion memory system may have any workflow
interface, and that choice is independent of the
