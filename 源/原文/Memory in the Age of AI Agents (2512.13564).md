---
source_url: https://arxiv.org/abs/2512.13564
source: arXiv 2512.13564
type: raw
created: 2026-07-06
tags: [学术论文, Agent记忆, 综述, raw]
---

# Memory in the Age of AI Agents

> arXiv: https://arxiv.org/abs/2512.13564
> PDF: 107页, 14.9MB (已下载至同目录 .pdf)
> 47位作者（NUS、人大、复旦、北大等）
> 提交: 2025-12-15，修订: 2026-01-13
> 入库日期: 2026-07-06
> 提取方式: pdftotext -layout → 纯文本提取
> GitHub: https://github.com/Shichun-Liu/Agent-Memory-Paper-List

                                             Memory in the Age of AI Agents: A Survey
                                             Forms, Functions and Dynamics
                                             Yuyang Hu† , Shichun Liu† , Yanwei Yue† , Guibin Zhang†ò , Boyang Liu , Fangyi Zhu , Jiahang Lin ,
                                             Honglin Guo , Shihan Dou , Zhiheng Xi , Senjie Jin , Jiejun Tan , Yanbin Yin , Jiongnan Liu , Zeyu Zhang ,
                                             Zhongxiang Sun , Yutao Zhu , Hao Sun , Boci Peng , Zhenrong Cheng , Xuanbo Fan , Jiaxin Guo , Xinlei Yu ,
                                             Zhenhong Zhou , Zewen Hu , Jiahao Huo , Junhao Wang , Yuwei Niu , Yu Wang , Zhenfei Yin , Xiaobin Hu ,
                                             Yue Liao , Qiankun Li , Kun Wang , Wangchunshu Zhou , Yixin Liu , Dawei Cheng , Qi Zhang , Tao Gui‡ ,
                                             Shirui Pan , Yan Zhang‡ , Philip Torr , Zhicheng Dou‡ , Ji-Rong Wen , Xuanjing Huang‡ , Yu-Gang Jiang ,
                                             Shuicheng Yan‡
                                              †
                                                  Core Contributors with Names Listed Alphabetically. ò Project Organizer. ‡ Core Supervisors.
arXiv:2512.13564v2 [cs.CL] 13 Jan 2026




                                             Affiliations: National University of Singapore, Renmin University of China, Fudan University,
                                             Peking University, Nanyang Technological University, Tongji University, University of California
                                             San Diego, Hong Kong University of Science and Technology (Guangzhou), Griffith University,
                                             Georgia Institute of Technology, OPPO, Oxford University

                                             Memory has emerged, and will continue to remain, a core capability of foundation model-based agents.
                                             It underpins long-horizon reasoning, continual adaptation, and effective interaction with complex
                                             environments. As research on agent memory rapidly expands and attracts unprecedented attention,
                                             the field has also become increasingly fragmented. Existing works that fall under the umbrella of
                                             agent memory often differ substantially in their motivations, implementations, assumptions, and
                                             evaluation protocols, while the proliferation of loosely defined memory terminologies has further
                                             obscured conceptual clarity. Traditional taxonomies such as long/short-term memory have proven
                                             insufficient to capture the diversity and dynamics of contemporary agent memory systems. This
                                             survey aims to provide an up-to-date and comprehensive landscape of current agent memory research.
                                             We begin by clearly delineating the scope of agent memory and distinguishing it from related concepts
                                             such as LLM memory, retrieval augmented generation (RAG), and context engineering. We then
                                             examine agent memory through the unified lenses of forms, functions, and dynamics. From the
                                             perspective of forms, we identify three dominant realizations of agent memory, namely token-level,
                                             parametric, and latent memory. From the perspective of functions, we move beyond coarse temporal
                                             categorizations and propose a finer-grained taxonomy that distinguishes factual, experiential, and
                                             working memory. From the perspective of dynamics, we analyze how memory is formed, evolved, and
                                             retrieved over time as agents interact with their environments. To support empirical research and
                                             practical development, we compile a comprehensive summary of representative benchmarks and open
                                             source memory frameworks. Beyond consolidation, we articulate a forward-looking perspective on
                                             emerging research frontiers, including automation-oriented memory design, the deep integration of
                                             reinforcement learning with memory systems, multimodal memory, shared memory for multi-agent
                                             systems, and trustworthiness issues. We hope this survey serves not only as a reference for existing
                                             work, but also as a conceptual foundation for rethinking memory as a first-class primitive in the design
                                             of future agentic intelligence.

                                             # Main Contact: guibinz@u.nus.edu, yuyang.hu@ruc.edu.cn, liusc24@m.fudan.edu.cn, ywyue25@stu.pku.edu.cn
                                              Github: https://github.com/Shichun-Liu/Agent-Memory-Paper-List




                                             Note: If you identify your own or other papers relevant to this survey that have not been discussed (we apologize for any
                                         such omissions due to the rapidly expanding literature), please feel free to contact us via email or raise an issue on GitHub.


                                                                                                       1
Contents

1 Introduction                                                                                                 4

2 Preliminaries: Formalizing Agents and Memory                                                                  6
  2.1 LLM-based Agent Systems . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         6
  2.2 Agent Memory Systems . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        7
  2.3 Comparing Agent Memory with Other Key Concepts . . . . . . . . . . . . . . . . . . . . . . .              8
       2.3.1 Agent Memory vs. LLM Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .            9
       2.3.2 Agent Memory vs. RAG . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        10
       2.3.3 Agent Memory vs. Context Engineering . . . . . . . . . . . . . . . . . . . . . . . . . .          11

3 Form: What Carries Memory?                                                                                   12
  3.1 Token-level Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     13
      3.1.1 Flat Memory (1D) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       15
      3.1.2 Planar Memory (2D) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       20
      3.1.3 Hierarchical Memory (3D) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       21
  3.2 Parametric Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      22
      3.2.1 Internal Parametric Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         22
      3.2.2 External Parametric Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         24
  3.3 Latent Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    26
      3.3.1 Generate . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     26
      3.3.2 Reuse . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    28
      3.3.3 Transform . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    28
  3.4 Adaptation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   30

4 Functions: Why Agents Need Memory?                                                                           31
  4.1 Factual Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     32
      4.1.1 User factual memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      35
      4.1.2 Environment factual memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         36
  4.2 Experiential Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    37
      4.2.1 Case-based Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        39
      4.2.2 Strategy-based Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        40
      4.2.3 Skill-based Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       41
      4.2.4 Hybrid memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      42
  4.3 Working Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     42
      4.3.1 Single-turn Working Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         43
      4.3.2 Multi-turn Working Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          45

5 Dynamics: How Memory Operates and Evolves?                                                                   46
  5.1 Memory Formation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     48
      5.1.1 Semantic Summarization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         48
      5.1.2 Knowledge Distillation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     50
      5.1.3 Structured Construction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      51
      5.1.4 Latent Representation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      53
      5.1.5 Parametric Internalization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     54
  5.2 Memory Evolution . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     55
      5.2.1 Consolidation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    55
      5.2.2 Updating . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     57
      5.2.3 Forgetting . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   58
  5.3 Memory Retrieval . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     59
      5.3.1 Retrieval Timing and Intent . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      60
      5.3.2 Query Construction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       62
      5.3.3 Retrieval Strategies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   62
      5.3.4 Post-Retrieval Processing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      64


                                                        2
6 Resources and Frameworks                                                                                    65
  6.1 Benchmarks and Datasets . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     65
      6.1.1 Benchmarks for Memory / Lifelong / Self-Evolving Agents . . . . . . . . . . . . . . .             65
      6.1.2 Other Related Benchmarks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        67
  6.2 Open-Source Frameworks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      68

7 Positions and Frontiers                                                                                     69
  7.1 Memory Retrieval vs. Memory Generation . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        69
      7.1.1 Look Back: From Memory Retrieval to Memory Generation . . . . . . . . . . . . . . .               69
      7.1.2 Future Perspective . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    69
  7.2 Automated Memory Management . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         70
      7.2.1 Look-Back: From Hand-crafted to Automatically Constructed Memory Systems. . . .                   70
      7.2.2 Future Perspective . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    70
  7.3 Reinforcement Learning Meets Agent Memory . . . . . . . . . . . . . . . . . . . . . . . . . . .         71
      7.3.1 Look-Back: RL is Internalizing Memory Management Abilities for Agents. . . . . . . .              71
      7.3.2 Future Perspective . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    72
  7.4 Multimodal Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     72
      7.4.1 Look-Back . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   72
      7.4.2 Future Perspective . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    73
  7.5 Shared Memory in Multi-Agent Systems . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        73
      7.5.1 Look-Back: From Isolated Memories to Shared Cognitive Substrates . . . . . . . . . .              73
      7.5.2 Future Perspective . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    73
  7.6 Memory for World Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      74
      7.6.1 Look-Back . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   74
      7.6.2 Future Perspective . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    74
  7.7 Trustworthy Memory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    75
      7.7.1 Look-Back: From Trustworthy RAG to Trustworthy Memory . . . . . . . . . . . . . .                 75
      7.7.2 Future Perspective . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    75
  7.8 Human-Cognitive Connections . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       76
      7.8.1 Look Back . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   76
      7.8.2 Future Perspective . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    76

8 Conclusion                                                                                                  76




                                                       3
Figure 1 Overview of agent memory organized by the unified taxonomy of forms (Section 3), functions (Section 4),
and dynamics (Section 5). The diagram positions memory artifacts by their dominant form and primary function. It
further maps representative systems into this taxonomy to provide a consolidated landscape.


1   Introduction
The past two years have witnessed the overwhelming evolution of increasingly capable large language models
(LLMs) into powerful AI agents (Matarazzo and Torlone, 2025; Minaee et al., 2025; Luo et al., 2025a).
These foundation-model-powered agents have demonstrated remarkable progress across diverse domains
such as deep research (Xu and Peng, 2025; Zhang et al., 2025p), software engineering (Wang et al., 2024i),
and scientific discovery (Wei et al., 2025c), continuously advancing the trajectory toward artificial general
interlligence (AGI) (Fang et al., 2025a; Durante et al., 2024). Although early conceptions of “agents” were
highly heterogeneous, a growing consensus has since emerged within the community: beyond a pure LLM
backbone, an agent is typically equipped with capabilities such as reasoning, planning, perception, memory, and
tool-use. Some of these abilities, such as reasoning and tool-use, have been largely internalized within model
parameters through reinforcement learning (Wang et al., 2025m; Qu et al., 2025b), while some still depend
heavily on external agentic scaffolds. Together, these components transform LLMs from static conditional
generators into learnable policies that can interact with diverse external environments and adaptively evolve
over time (Zhang et al., 2025f; Liu et al., 2025a).
Among these agentic faculties, memory stands out as a cornerstone, explicitly enabling the transformation
of static LLMs, whose parameters cannot be rapidly updated, into adaptive agents capable of continual
adaptation through environmental interaction (Zhang et al., 2025s; Wu et al., 2025g). From an application
perspective, numerous domains demand agents with proactive memory management rather than ephemeral,
forgetful behaviors: personalized chatbots (Chhikara et al., 2025; Li et al., 2025b), recommender systems (Liu
et al., 2025c), social simulations (Park et al., 2023; Yang et al., 2025), and financial investigations (Zhang
et al., 2024) all rely on the agent’s ability to process, store, and manage historical information. From a
developmental standpoint, one of the defining aspirations of AGI research is to endow agents with the capacity
for continual evolution through environment interactions (Hendrycks et al., 2025), a capability fundamentally


                                                       4
grounded in agent memory.

Agent Memory Needs A New Taxonomy Given the growing significance and community attention
surrounding agent memory systems, it has become both timely and necessary to provide an updated perspective
on contemporary agent memory research. The motivation for a new taxonomy and survey is twofold: ❶
Limitations of Existing Taxonomies: While several recent surveys have provided valuable and comprehensive
overviews of agent memory (Zhang et al., 2025s; Wu et al., 2025g), their taxonomies were developed prior to a
number of rapid methodological advances and therefore do not fully reflect the current breadth and complexity
of the research landscape. For example, emerging directions in 2025, such as memory frameworks that distill
reusable tools from past experiences (Qiu et al., 2025a,c; Zhao et al., 2025c), or memory-augmented test-time
scaling methods (Zhang et al., 2025g; Suzgun et al., 2025), remain underrepresented in earlier classification
schemes. ❷ Conceptual Fragmentation: With the explosive growth of memory-related studies, the concept
itself has become increasingly expansive and fragmented. Researchers often find that papers claiming to study
“agent memory” differ drastically in implementation, objectives, and underlying assumptions. The proliferation
of diverse terminologies (declarative, episodic, semantic, parametric memory, etc.) further obscures conceptual
clarity, highlighting the urgent need for a coherent taxonomy that can unify these emerging concepts.
Therefore, this paper seeks to establish a systematic framework that reconciles existing definitions, bridges
emerging trends, and elucidates the foundational principles of memory in agentic systems. Specifically, this
survey aims to address the following key questions:

  Key Questions

 ❶ How is agent memory defined, and how does it relate to related concepts such as LLM memory,
   retrieval-augmented generation (RAG), and context engineering?
 ❷ Forms: What architectural or representational forms can agent memory take?
 ❸ Functions: Why is agent memory needed, and what roles or purposes does it serve?
 ❹ Dynamics: How does agent memory operate, adapt, and evolve over time?
 ❺ What are the promising frontiers for advancing agent memory research?


To address question ❶, we first provide formal definitions for LLM-based agents and agent memory systems
in Section 2, and present a detailed comparison between agent memory and related concepts such as LLM
memory, RAG, and context engineering. Following the “Forms–Functions–Dynamics” triangle, we offer a
structured overview of agent memory. Question ❷ examines the architectural forms of memory, which we
discuss in Section 3, highlighting three mainstream implementations: token-level, parametric, and latent
memory. Question ❸ concerns the functional roles of memory, addressed in Section 4, where we distinguish
between factual memory, which records knowledge from agents’ interactions with users and the environment;
experiential memory, which incrementally enhances the agent’s problem-solving capabilities through task
execution; and working memory, which manages workspace information during individual task instances.
Question ❹ focuses on the lifecycle and operational dynamics of agent memory, which we present sequentially
in terms of memory formulation, retrieval, and evolution.
After surveying existing research through the lenses of “Forms–Functions–Dynamics,” we further provide our
perspectives and insights on agent memory research. To facilitate knowledge sharing and future development,
we first summarize key benchmarks and framework resources in Section 6. Building upon this foundation, we
then address question ❺ by exploring several emerging yet underdeveloped research frontiers in Section 7,
including automation-oriented memory design, the integration of reinforcement learning (RL), multimodal
memory, shared memory for multi-agent systems, and trustworthy issues.

Contributions The contributions of this survey can be summarized as follows: (1) We present an up-to-
date and multidimensional taxonomy of agent memory from the perspective of “forms–functions–dynamics,”
offering a structured lens through which to understand current developments in the field. (2) We provide
an in-depth discussion on the suitability and interplay of different memory forms and functional purposes,


                                                      5
offering insights into how various memory types can be effectively aligned with distinct agentic objectives.
(3) We investigate emerging and promising research directions in agent memory, thereby outlining future
opportunities and guiding pathways for advancement. (4) We compile a comprehensive collection of resources,
including benchmarks and open-source frameworks, to support both researchers and practitioners in further
exploration of agent memory systems.

Outline of the Survey The remainder of this survey is organized as follows. Section 2 formalizes LLM-based
agents and agent memory systems, and clarifies their relationships with related concepts. Section 3, Section 4,
and Section 5 respectively examine the forms, functions, and dynamics of agent memory. Section 6 summarizes
representative benchmarks and framework resources. Section 7 discusses emerging research frontiers and
future directions. Finally, we conclude the survey with a summary of key insights in Section 8.


2     Preliminaries: Formalizing Agents and Memory
LLM agents increasingly serve as the decision-making core of interactive systems that operate over time,
manipulate external tools, and coordinate with humans or other agents. To study memory in such settings,
we begin by formalizing LLM-based agent systems in a manner that encompasses both single-agent and
multi-agent configurations. We then formalize the memory system coupled to the agent’s decision process
through read/write interactions, enabling a unified treatment of memory phenomena that arise both within a
task (inside-trial / short-term memory) and across tasks (cross-trial / long-term memory).

2.1   LLM-based Agent Systems
Agents and Environment Let I = {1, . . . , N } denote the index set of agents, where N = 1 corresponds
to the single-agent case (e.g., ReAct), and N > 1 represents multi-agent settings such as debate (Li et al.,
2024c) or planner–executor architectures (Wan et al., 2025). The environment is characterized by a state
space S. At each time step t, the environment evolves according to a controlled stochastic transition model

                                            st+1 ∼ Ψ(st+1 | st , at ),

where at denotes the action executed at time t. In multi-agent systems, this abstraction allows for ei-
ther sequential decision-making (where a single agent acts at each step) or implicit coordination through
environment-mediated effects. Each agent i ∈ I receives an observation

                                               oit = Oi (st , hit , Q),

where hit denotes the portion of the interaction history visible to agent i. This history may include previous
messages, intermediate tool outputs, partial reasoning traces, shared workspace states, or other agents’
contributions, depending on the system design. Q denotes the task specification, such as a user instruction,
goal description, or external constraints, which is treated as fixed within a task unless otherwise specified.

Action Space A distinguishing feature of LLM-based agents is the heterogeneity of their action space.
Rather than restricting actions to plain text generation, agents may operate over a multimodal and semantically
structured action space, including:
 • Natural-language generation, such as producing intermediate reasoning, explanations, responses, or instruc-
   tions (Li et al., 2023b; Wu et al., 2024b; Hong et al., 2024; Qian et al., 2024).
 • Tool invocation actions, which call external APIs, search engines, calculators, databases, simulators, or code
   execution environments (Qin et al., 2025; Li et al., 2025h; Zhou et al., 2023c, 2024c).
 • Planning actions, which explicitly output task decompositions, execution plans, or subgoal specifications to
   guide later behavior (CAMEL-AI, 2025; Liu et al., 2025g; Pan et al., 2024).
 • Environment-control actions, where the agent directly manipulates the external environment (e.g., navigation
   in embodied settings (Shridhar et al., 2021; Wang et al., 2022a), editing a software repository (Jimenez
   et al., 2024; Aleithan et al., 2024), or modifying a shared memory buffer).


                                                          6
 • Communication actions, enabling collaboration or negotiation with other agents through structured
   messages (Marro et al., 2024).
These actions, though diverse in semantics, are unified by the fact that they are produced through an
autoregressive LLM backbone conditioned on a contextual input. Formally, each agent i follows a policy

                                                  at = πi (oit , mit , Q),

where mit is a memory-derived signal defined in Section 2.2. The policy may internally generate multi-step
reasoning chains, latent deliberation, or scratchpad computations prior to emitting an executable action; such
internal processes are abstracted away and not explicitly modeled.

Interaction Process and Trajectories             A full execution of the system induces a trajectory

                                        τ = (s0 , o0 , a0 , s1 , o1 , a1 , . . . , sT ),

where T is determined by task termination conditions or system-specific stopping criteria. At each step,
the trajectory reflects the interleaving of (i) environment observation, (ii) optional memory retrieval, (iii)
LLM-based computation, and (iv) action execution that drives the next state transition.
This formulation captures a broad class of agentic systems, ranging from a single agent solving reasoning
tasks with tool augmentation to teams of role-specialized agents collaboratively developing software (Qian
et al., 2024; Wang et al., 2025l) or conducting scientific inquiry (Weng et al., 2025). We next formalize the
memory systems that integrate into this agent loop.

2.2   Agent Memory Systems
While an LLM-based agent interacts with an environment, its instantaneous observation oit is often insufficient
for effective decision-making. Agents therefore rely on additional information derived from prior interactions,
both within the current task and across previously completed tasks. We formalize this capability through a
unified agent memory system, represented as an evolving memory state

                                                         Mt ∈ M,

where M denotes the space of admissible memory configurations. No specific internal structure is imposed
on Mt ; it may take the form of a text buffer, key–value store, vector database, graph structure, or any
hybrid representation. At the beginning of a task, Mt may already contain information distilled from prior
trajectories (cross-trial memory). During task execution, new information accumulates and functions as
short-term, task-specific memory. Both roles are supported within a single memory container, with temporal
distinctions emerging from usage patterns rather than architectural separation.

Memory Lifecycle: Formation, Evolution, and Retrieval The dynamics of the memory system are
characterized by three conceptual operators.
Memory Formation At time step t, the agent produces informational artifacts ϕt , which may include tool
outputs, reasoning traces, partial plans, self-evaluations, or environmental feedback. A formation operator

                                                 Mform
                                                  t+1 = F (Mt , ϕt )

selectively transforms these artifacts into memory candidates, extracting information with potential future
utility rather than storing the entire interaction history verbatim.
Memory Evolution Formed memory candidates are integrated into the existing memory base through an
evolution operator
                                                 Mt+1 = E(Mform
                                                           t+1 ),

which may consolidate redundant entries (Zhao et al., 2024), resolve conflicts (Rasmussen et al., 2025; Li
et al., 2025l), discard low-utility information (Wang et al., 2025r), or restructure memory for efficient retrieval.
The resulting memory state persists across subsequent decision steps and tasks.


                                                               7
Memory Retrieval When selecting an action, agent i retrieves a context-dependent memory signal

                                             mit = R(Mt , oit , Q),

where R denotes a retrieval operator that constructs a task-aware query and returns relevant memory content.
The retrieved signal mit is formatted for direct consumption by the LLM policy, for example as a sequence of
textual snippets or a structured summary.

Temporal Roles Within the Agent Loop Although memory is represented as a unified state Mt , the
three lifecycle operators (formation F , evolution E, and retrieval R) need not be invoked at every time step.
Instead, different memory effects arise from distinct temporal invocation patterns. For instance, some systems
perform retrieval only once at task initialization,
                                               (
                                           i
                                                 R(M0 , oi0 , Q), t = 0,
                                         mt =
                                                 ⊥,               t > 0,

where ⊥ denotes null retrieval strategy. Others may retrieve memory intermittently or continuously based on
contextual triggers. Similarly, memory formation may range from minimal accumulation of raw observations,

                                             Mform         i
                                              t+1 = Mt ∪ {ot },

to sophisticated extraction and refinement of reusable patterns or abstractions. Thus, inside a task, short-term
memory effects may arise from lightweight logging just as in Yao et al. (2023b); Chen et al. (2023a) or from
more elaborate iterative refinement (Hu et al., 2025a); across tasks, long-term memory may be updated
episodically at task boundaries or continuously throughout operation. Short-term and long-term memory
phenomena therefore emerge not from discrete architectural modules but from the temporal patterns with
which formation, evolution, and retrieval are engaged.

Memory–Agent Coupling The interaction between memory and the agent’s decision process is similarly
flexible. In general, the agent policy is written as

                                              at = πi (oit , mit , Q),

where the retrieved memory signal mit may be present or absent depending on the retrieval schedule. When
retrieval is disabled at a given step, mit can be treated as a distinguished null input.
Consequently, the overall agent loop consists of observing the environment, optionally retrieving memory,
computing an action, receiving feedback, and optionally updating memory through formation and evolu-
tion. Different agent implementations instantiate different subsets of these operations at different temporal
frequencies, giving rise to memory systems that range from passive buffers to actively evolving knowledge
bases.

2.3   Comparing Agent Memory with Other Key Concepts
Despite the growing interest in agentic systems endowed with memory, the community’s understanding of what
constitutes agent memory remains fragmented. In practice, researchers and practitioners often conflate agent
memory with related constructs such as LLM memory (Wu et al., 2025g), retrieval-augmented generation
(RAG) (Gao et al., 2024), and context engineering (Mei et al., 2025). Although these concepts are intrinsically
connected by their involvement in how information is managed and utilized in LLM-driven systems, they
differ in scope, temporal characteristics, and functional roles.
These overlapping yet distinct notions have led to ambiguity in the literature and practice. To clarify these
distinctions and situate agent memory within this broader landscape, we examine how agent memory relates
to, and diverges from, LLM memory, RAG, and context engineering in the subsequent subsubsections. Figure 2
visually illustrates the commonalities and distinctions among these fields through a Venn diagram.



                                                         8
        - Self-Evolving Memory
          e.g., Memento, H2R           - Parametric Memory
                                                                                  - Few-shot prompting
        - Multimodal Memory              e.g., Retroformer, Early experience
                                                                                    e.g., CoT, PALM
         e.g., Ella, ViloMem, M3-Agent - RL-enabled Memory
                                                                                  - Self-Reflection
        - Latent Memory                 e.g., MemAgent, RMM, MemSearcher,
                                                                                   e.g., Self-refine, CRITIC
          e.g., MemoryLLM, M+, MemGen MEM1, Mem-alpha, Memory-R1                  - KV compression/reuse
                                                                                    e.g., AutoCompressor, SnapKV



                                                      Agent                                      - Attention KV management
        - Memory graph                                                                             e.g., Mixture-of-Memory
          e.g., Zep, AriGraph                        Memory
                                                                                                 - Long context processing
        - Agentic memory                                                        LLM               e.g., Mamba, Memformer, MoA,
          e.g., A-Mem, G-Memory                                                Memory            Sparseformer, NSA
        - Working memory
          e.g., HiAgent, ReSum,



                                                                                  - Tool-integrated reasoning
                                        RAG                                        e.g., ReTool, ToolLLM,
 - Modular RAG                                               Context              Toolformer, VTool-R1, ToRL
  e.g., FlashRAG, ComposeRAG
 - Graph RAG                                               Engineering            - Tool selection
  e.g., LightRAG, HippoRAG                                                         e.g., AutoTool, VisTA
 - Agentic RAG                                                                    - Communication protocol
   e.g., PlanRAG, Self-RAG                                                          e.g., ANP, A2A, MCP, Agora


Figure 2 Conceptual comparison of Agent Memory with LLM Memory, RAG, and Context Engineering. The diagram
illustrates shared technical implementations (e.g., KV reuse, graph retrieval) while highlighting fundamental distinctions:
unlike the architectural optimizations of LLM Memory, the static knowledge access of RAG, or the transient resource
management of Context Engineering, Agent Memory is uniquely characterized by its focus on maintaining a persistent
and self-evolving cognitive state that integrates factual knowledge and experience. The listed categories and examples
are illustrative rather than strictly parallel, serving as representative reference points to clarify conceptual relationships
rather than to define a rigid taxonomy.


2.3.1    Agent Memory vs. LLM Memory

At a high level, agent memory almost fully subsumes what has traditionally been referred to as LLM memory.
Since 2023, many works describing themselves as “LLM memory mechanisms” (Zhong et al., 2024; Packer
et al., 2023a; Wang et al., 2023b) are more appropriately interpreted, under contemporary terminology, as
early instances of agent memory. This reinterpretation arises from the historical ambiguity surrounding the
very notion of an “LLM agent.” During 2023–2024, the community had no stable or coherent definition: in
some cases, prompting an LLM to call a calculator already sufficed to qualify the system as an agent (Wu
et al., 2024c); in other cases, agency required substantially richer capabilities such as explicit planning, tool
use, memory, and reflective reasoning (Ruan et al., 2023). Only recently has a more unified and structured
definition begun to emerge (e.g., LLM-based agent = LLM + reasoning + planning + memory + tool use
+ self-improvement + multi-turn interaction + perception, as discussed by Zhang et al. (2025f)), though
even this formulation is not universally applicable. Against this historical backdrop, early systems such
as MemoryBank (Zhong et al., 2024) and MemGPT (Packer et al., 2023a) framed their contributions as
providing LLM memory. Yet what they fundamentally addressed were classical agentic challenges, for example
enabling an LLM-based conversational agent to track user preferences, maintain dialogue-state information,
and accumulate experience across multi-turn interactions. Under a modern and more mature understanding
of agency, such systems are naturally categorized as instances of agent memory.
That said, the subsumption is not absolute. A distinct line of research genuinely concerns LLM-internal
memory: managing the transformer’s key–value (KV) cache, designing long-context processing mechanisms,
or modifying model architectures (e.g., RWKV (Peng et al., 2023), Mamba (Gu and Dao, 2024; Lieber et al.,
2024), diffusion-based LMs (Nie et al., 2025)) to better retain information as sequence length grows. These
works focus on intrinsic model dynamics and typically address tasks that do not require agentic behavior, and
thus should be considered outside the scope of agent memory.



                                                                  9
Overlap Within our taxonomy, the majority of what has historically been called “LLM memory” corresponds
to forms of agent memory. Techniques such as few-shot prompting (Prabhumoye et al., 2022; Ma et al., 2023a)
can be viewed as a form of long-term memory, where past exemplars or distilled task summaries serve as
reusable knowledge incorporated through retrieval or context injection. Self-reflection and iterative refinement
methods (Madaan et al., 2023; Mousavi et al., 2023; Han et al., 2025c) naturally align with short-term,
inside-trial memory, as the agent repeatedly leverages intermediate reasoning traces or outcomes from prior
attempts within the same task. Even KV compression and context-window management (Yoon et al., 2024;
Jiang et al., 2023), when used to preserve salient information across the course of a single task, function
as short-term memory mechanisms in an agentic sense. These techniques all support the agent’s ability to
accumulate, transform, and reuse information throughout a task’s execution.

Distinctions In contrast, memory mechanisms that intervene directly in the model’s internal state—such as
architectural modifications for longer effective context, cache rewriting strategies, recurrent-state persistence,
attention-sparsity mechanisms, or externalized KV-store expansions—are more appropriately classified as
LLM memory rather than agent memory. Their goal is to expand or reorganize the representational capacity
of the underlying model, not to furnish a decision-making agent with an evolving external memory base.
They do not typically support cross-task persistence, environment-driven adaptation, or deliberate memory
operations (e.g., formation, evolution, retrieval), and therefore lie outside the operational scope of agent
memory as defined in this survey.

2.3.2   Agent Memory vs. RAG

At a conceptual level, agent memory and retrieval-augmented generation (RAG) exhibit substantial overlap:
both systems construct, organize, and leverage auxiliary information stores to extend the capabilities of
LLM/agents beyond their native parametric knowledge. For instance, structured representations such as
knowledge graphs and indexing strategies appear in both communities’ methods, and recent developments in
agentic RAG demonstrate how autonomous retrieval mechanisms can interact with dynamic databases in ways
reminiscent of agent memory architectures (Singh et al., 2025). Indeed, the engineering stacks underlying
many RAG and agent memory systems share common building blocks, including vector indices, semantic
search, and context expansion modules.
Despite these technological convergences, the two paradigms have historically been distinguished by the
contexts in which they are applied. Classical RAG techniques primarily augment an LLM with access to static
knowledge sources, whether flat document stores, structured knowledge bases, or large corpora externally
indexed to support retrieval on demand (Zhang et al., 2025q; Han et al., 2025b). These systems are designed
to ground generation in up-to-date facts, mitigate hallucinations, and improve accuracy in knowledge-intensive
tasks, but they generally do not maintain an internal, evolving memory of past interactions. In contrast,
agent memory systems are instantiated within an agent’s ongoing interaction with an environment, continuously
incorporating new information generated by the agent’s own actions and environmental feedback into a
persistent memory base (Wang et al., 2024m; Zhao et al., 2024; Sun et al., 2025e).
In early formulations the distinction between RAG and agent memory was relatively clear: RAG retrieved from
externally maintained knowledge for a single task invocation, whereas agent memory evolved over multi-turn,
multi-task interaction. However, this boundary has become increasingly blurred as retrieval systems themselves
become more dynamic. For example, certain retrieval tasks continuously update relevant context during
iterative querying (e.g., multi-hop QA settings where related context is progressively added). Interestingly,
systems such as HippoRAG/HippoRAG2 (Gutierrez et al., 2024; Gutiérrez et al., 2025) have been interpreted
by both RAG and memory communities as addressing long-term memory challenges for LLMs. Consequently,
a more practical (though not perfectly separable) distinction lies in the task domain. RAG is predominantly
applied to augment LLMs with large, externally sourced context for individual inference tasks, exemplified by
classical multi-hop and knowledge-intensive benchmarks such as HotpotQA (Yang et al., 2018), 2WikiMQA (Ho
et al., 2020), and MuSiQue (Trivedi et al., 2022). By contrast, agent memory systems are typically evaluated
in settings requiring sustained multi-turn interaction, temporal dependency, or environment-driven adaptation.
Representative benchmarks include long-context dialogue evaluations such as LoCoMo (Maharana et al.,
2024) and LongMemEval (Wu et al., 2025a), complex problem-solving and deep-research benchmarks such as
GAIA (Mialon et al., 2023), XBench (Chen et al., 2025c), and BrowseComp (Wei et al., 2025b), code-centric


                                                       10
agentic tasks such as SWE-bench Verified (Jimenez et al., 2024), as well as lifelong learning benchmarks such
as StreamBench (Wu et al., 2024a). We provide a comprehensive summary of memory-related benchmarks in
Section 6.1.
Nevertheless, even this domain-based distinction contains substantial gray areas. Many works self-described as
agent memory systems are evaluated under long-document question-answering tasks such as HotpotQA (Wang
et al., 2025g,p), while numerous papers foregrounded as RAG systems in fact implement forms of agentic self-
improvement, continually distilling and refining knowledge or skills over time. As a result, titles, methodologies,
and empirical evaluations frequently blur the conceptual boundary between the two paradigms. To further
clarify these relationships, the following three paragraphs draw upon established taxonomies of RAG from (Mei
et al., 2025): modular RAG, graph RAG, and agentic RAG, and examine how the core techniques associated
with each lineage manifest within both RAG and agent memory systems.

Modular RAG Modular RAG refers to architectures in which the retrieval pipeline is decomposed into
clearly specified components, such as indexing, candidate retrieval, reranking, filtering, and context assembly,
that operate in a largely static and pipeline-like fashion (Singh et al., 2025). These systems treat retrieval as a
well-engineered, modular subsystem external to the LLM, designed primarily for injecting relevant knowledge
into the model’s context window during inference. Within the agent memory perspective, the corresponding
techniques typically appear in the retrieval stage, where memory access is realized through vector search,
semantic similarity matching, or rule-based filtering, as seen in popular agent memory frameworks like
Memary (Memary, 2025), MemOS (Li et al., 2025l), and Mem0 (Chhikara et al., 2025).

Graph RAG Graph RAG systems structure the knowledge base as a graph, ranging from knowledge
graphs to concept graphs or document-entity relations, and leverage graph traversal or graph-based ranking
algorithms to retrieve context (Peng et al., 2024). This representation enables multi-hop relational reasoning,
which has proven effective for knowledge-intensive tasks (Edge et al., 2025; Han et al., 2025b; Dong et al.,
2025a). In the context of agent memory, graph-structured memory arises naturally when agents accumulate
relational insights over time, such as linking concepts, tracking dependencies among subtasks, or recording
causal relations inferred through interaction. Several well-established practices include Mem0g (Chhikara et al.,
2025), A-MEM (Xu et al., 2025c), Zep (Rasmussen et al., 2025), and G-memory (Zhang et al., 2025c). Notably,
graph-based agent memory systems may construct, extend, or reorganize its internal graph throughout the
agent’s operation. Consequently, graph-based retrieval forms the structural backbone for both paradigms, but
only agent memory treats the graph as a living, evolving representation of experience. We provide further
analysis on graph-based memory forms in Section 3.1.2 and also refer the readers to a relevant survey (Liu
et al., 2025h).

Agentic RAG Agentic RAG integrates retrieval into an autonomous decision-making loop, where an LLM
agent actively controls when, how, and what to retrieve (Singh et al., 2025; Sun et al., 2025e). These systems
often employ iterative querying, multi-step planning, or self-directed search procedures, enabling the agent to
refine its information needs through deliberate reasoning, as implemented in PlanRAG (Lee et al., 2024b)
and Self-RAG (Asai et al., 2023). For a more detailed understanding of agentic RAG, we refer the readers to
Singh et al. (2025). From the agent memory perspective, agentic RAG occupies the closest conceptual space:
both systems involve autonomous interaction with an external information store, both support multi-step
refinement, and both may incorporate retrieved insights into subsequent reasoning. The key distinction is
that classical agentic RAG typically operates over an external and often task-specific database, whereas agent
memory maintains an internal, persistent, and self-evolving memory base that accumulates knowledge across
tasks (Yan et al., 2025b; Xu et al., 2025c).

2.3.3   Agent Memory vs. Context Engineering

The relationship between agent memory and context engineering is best understood as an intersection of
distinct operational paradigms rather than a hierarchical subsumption. Context engineering is a systematic
design methodology that treats the context window as a constrained computational resource. It rigorously
optimizes the information payload, including instructions, knowledge, state, and memory, to mitigate the
asymmetry between massive input capacity and the model’s generation capability (Mei et al., 2025). While


                                                        11
agent memory focuses on the cognitive modeling of a persistent entity with an evolving identity, context
engineering operates under a resource management paradigm. From the perspective of context engineering,
agent memory is merely one variable within the context assembly function that requires efficient scheduling to
maximize inference efficacy. Conversely, from the perspective of an agent, context engineering serves as the
implementation layer that ensures cognitive continuity remains within the physical limits of the underlying
model.

Overlap The two fields converge significantly in the technical realization of working memory during long-
horizon interactions and often employ functionally identical mechanisms to address the constraints imposed
by a finite context window (Hu et al., 2025a; Zhang et al., 2025r; Kang et al., 2025c; Yu et al., 2025a). Both
paradigms rely on advanced information compression (Zhou et al., 2025b; Wu et al., 2025f), organization (Xu
et al., 2025c; Zhang et al., 2025c; Anokhin et al., 2024), and selection (Zhang et al., 2025r) techniques
to preserve operational continuity over extended interaction sequences. For example, token pruning and
importance-based selection methods (Jiang et al., 2023; Li et al., 2023c) that are central to context engineering
frameworks play a fundamental role in agentic memory systems by filtering noise and retaining salient
information. Similarly, the rolling summary technique serves as a shared foundational primitive, functioning
simultaneously as a buffer management strategy and a transient episodic memory mechanism (Yu et al., 2025a;
Lu et al., 2025b). In practice, the boundary between engineering the context and maintaining an agent’s
short-term memory effectively dissolves in these scenarios, as both rely on the same underlying summarization,
dynamic information retrieval, and recursive state updates (Tang et al., 2025b; Yoon et al., 2024).

Distinctions The distinction becomes most pronounced when moving beyond short-term text processing to
the broader scope of long-lived agents. Context engineering primarily addresses the structural organization
of the interaction interface between LLMs and their operational environment. This includes optimizing
tool-integrated reasoning and selection pipelines (Qin et al., 2024a; Schick et al., 2023; Jia and Li, 2025)
and standardizing communication protocols, such as MCP (Qiu et al., 2025c). These methods focus on
ensuring that instructions, tool calls, and intermediate states are correctly formatted, efficiently scheduled,
and executable within the constraints of the context window. As such, context engineering operates at the
level of resource allocation and interface correctness, emphasizing syntactic validity and execution efficiency.
In contrast, agent memory defines a substantially broader cognitive scope. Beyond transient context assembly,
it encompasses the persistent storage of factual knowledge (Zhong et al., 2024), the accumulation and
evolution of experiential traces (Zhao et al., 2024; Tang et al., 2025d; Zhang et al., 2025d), and, in some
cases, the internalization of memory into model parameters (Wang et al., 2025o). Rather than managing how
information is presented to the model at inference time, agent memory governs what the agent knows, what it
has experienced, and how these elements evolve over time. This includes consolidating repeated interactions
into knowledge (Tan et al., 2025c), abstracting procedural knowledge from past successes and failures (Ouyang
et al., 2025), and maintaining a coherent identity across tasks and episodes (Wang et al., 2024f).
From this perspective, context engineering constructs the external scaffolding that enables perception and
action under resource constraints, whereas agent memory constitutes the internal substrate that supports
learning, adaptation, and autonomy. The former optimizes the momentary interface between the agent and the
model, while the latter sustains a persistent cognitive state that extends beyond any single context window.


3   Form: What Carries Memory?
As a starting point for organizing prior work, we begin by examining the most fundamental representational
units out of which agent memory can be constructed. We first try to answer: what architectural or
representational forms can agent memory take?
Across diverse agent systems, memory is not realized through a single, unified structure. Instead, different
task settings call for different storage forms, each with its own structural properties. These architectures
endow memory with distinct capabilities, shaping how an agent accumulates information over interactions and
maintains behavioral consistency. They ultimately enable memory to fulfill its intended roles across varied
task scenarios.


                                                       12
Based on where memory resides and in what form it is represented, we organize these memories into three
categories:

  Three Major Memory Forms

      1. Token-level Memory (Section 3.1): Memory organized as explicit and discrete units that can be
         individually accessed, modified, and reconstructed. These units remain externally visible and can
         be stored in a structured form over time.
      2. Parametric Memory (Section 3.2): Memory stored within the model parameters, where information
         is encoded through the statistical patterns of the parameter space and accessed implicitly during
         forward computation.
      3. Latent Memory (Section 3.3): Memory represented in the model’s internal hidden states, continuous
         representations, or evolving latent structures. It can persist and update during inference or across
         interaction cycles, capturing context-dependent internal states.

The three memory forms outlined above establish the core structural framework for understanding “what
carries memory”. Each form organizes, stores, and updates information in its own way, giving rise to distinct
representational patterns and operational behaviors. With this structural taxonomy in place, we can more
systematically examine why agents need memory (Section 4) and how memory evolves, adapts, and shapes
agent behavior over sustained interactions (Section 5). This classification provides the conceptual foundation
for the discussions that follow.

3.1   Token-level Memory

  Definition of Token-level Memory

  Token-level memory stores information as persistent, discrete units that are externally accessible and
  inspectable. The token here is a broad representational notion: beyond text tokens, it includes visual
  tokens, audio frames—any discrete element that can be written, retrieved, reorganized, and revised
  outside model parameters.

Because these units are explicit, token-level memory is typically transparent, easy to edit, and straightforward
to interpret, making it a natural layer for retrieval, routing, conflict handling, and coordination with parametric
and latent memory. Token-level memory is also the most common memory form and the one with the largest
body of existing work.
Although all token-level memories share the property of being stored as discrete units, they differ significantly in
how these units are organized. The structural organization of stored tokens plays a central role in determining
how efficiently the agent can search, update, or reason over past information. To describe these differences,
we categorize token-level memory by inter-unit structural organization, moving from no explicit topology to
multi-layer topologies:

  Three Major Types of Token-level Memory

      1. Flat Memory (1D): No explicit inter-unit topology. Memories are accumulated as sequences or bags
         of units (e.g., snippets, trajectories, chunks)
      2. Planar Memory (2D): A structured but single-layer organization within one plane: units are related
         by a graph, tree, table and so on, with no cross-layer relations. The structure is explicit, but not
         layered.
      3. Hierarchical Memory (3D): Structured across multiple layers with inter-layer links, forming a volu-
         metric or stratified memory




                                                        13
      Experience                              Graph         Memory graphs with        Pyramid
                             ...                       different node/edge types

                                                     image            chat
      e.g., ExpeL, AWM, ReasoningBank


      Chunk
                            ...

      e.g., Nemori, Mem0, MemOS
                                                                                      e.g., G-Memory, CAM, others
                                               e.g., A-Mem, Mem0^g,
      Dialogue                                 M3-Agent, D-SMART
                                                                                      Multi-Layer
                            ...
                                              Tree                                                                  docs
      e.g., MemGPT, MemoryBank




                                                                                                                     ... ...
      Summary
                             ...
                                                                                                                QAs
      e.g., Think-in-Memory, RMM              e.g., MemTree, TME, others               HiAgent, HippoRAG, SGMem

      (a) Flat Memory (1D)                  (b) Planar Memory (2D)                     (c) Hierarchical (3D)

Figure 3 Taxonomy of token-level memory organized by topological complexity and dimensionality: (a) Flat Memory
(1D) stores information as linear sequences or independent clusters without explicit inter-unit topology, commonly
used for Chunk sets, Dialogue logs, and Experience pools. (b) Planar Memory (2D) introduces a single-layer structured
layout where units are linked via Tree or Graph structures to capture relational dependencies, supporting diverse node
types such as images and chat records. (c) Hierarchical Memory (3D) employs multi-level forms, such as Pyramids or
Multi-layer graphs, to facilitate vertical abstraction and cross-layer reasoning between different data granularities, such
as raw docs and synthesized QAs.


The three types of token-level memory are clearly illustrated in Figure 3. From Flat Memory with no
topology, to Planar Memory with single-layer structural organization, to Hierarchical Memory with multi-layer
interlinked structures, this organizational spectrum governs not only how token-level memory supports search,
update, and reasoning, but also how the memory itself is structured and what capabilities it affords. In the
subsections that follow, we introduce each organizational form in terms of its strengths and limitations, typical
use cases, and representative work. The summary and comparison of representative token-level memory
methods are presented in Table 1.
It is worth noting that, following the idea introduced by ReAct (Yao et al., 2023b), a series of studies began
focusing on long-horizon interaction tasks (Song et al., 2025a; Jin et al., 2025; Li et al., 2025h,e,j; Wu et al.,
2025b). Many of these tasks introduce an explicit notion of memory, and because the memory is generally
stored in plaintext form, they fall within the scope of token-level memory. Most of them emphasize how
to compress or fold accumulated interaction traces so that agents can operate over long sequences without
exceeding context limits (Zhou et al., 2025b; Zhang et al., 2025r; Wu et al., 2025f; Sun et al., 2025b; Li et al.,
2025i; Chen et al., 2025b). A more detailed discussion is provided in Section 4.3 about working memory.




                                                             14
3.1.1   Flat Memory (1D)


  Definition of Flat (1D) Memory

  Flat Memory stores information as accumulations of discrete units, without explicitly modeling semantic
  or relational dependencies among them. These units may include text chunks, user profiles, experience
  trajectories, their corresponding vector representations, or multimodal entries. Relationships among these
  units are not encoded directly in the memory.

To facilitate a clear and coherent presentation, we group prior work on flat memory according to their primary
design objectives and technical emphases. This grouping serves an organizational purpose and does not imply
that the resulting categories are strictly parallel or mutually exclusive. In practice, certain methods may be
applicable to multiple categories, and some approaches involving multimodal information may be discussed in
other sections when multimodality is not their central focus. Such an organization allows us to systematically
review the literature while preserving flexibility in interpretation.

Table 1 Comparison of representative token-level memory methods. We categorize existing works into three groups based
on their topological complexity: Flat Memory (1D) for linear or independent records, Planar Memory (2D) for structured
single-layer graphs/trees, and Hierarchical Memory (3D) for multi-level architectures. Methods are characterized across
four dimensions: (1) Multi indicates multimodal capability, where ✔ denotes support for modalities beyond text (e.g.,
visual) and ✗ implies text-only; (2) Type identifies the specific functional category of the memory (e.g., Fact for factual
memory, Exp for experiential memory, Work for working memory ); (3) Memory Form details the content of the stored
units; and (4) Task lists the primary application domains.

 Method                                    Multi   Type                  Memory Form                   Task
                                                         Flat Memory Models
 Reflexion (Shinn et al., 2023b)           ✗       E&W      Trajectory as short-term and feedback as   QA, Reasoning, Coding
                                                            long-term
 Memento (Zhou et al., 2025a)              ✗       Exp      Trajectory case (success/failure).       Reasoning
 JARVIS-1 (Wang et al., 2025q)             ✔       Exp      Plan-environment pairs.                  Game
 Expel (Zhao et al., 2024)                 ✗       Exp      Insights and few-shot examples.          Reasoning
 Buffer of Thoughts (Yang et al., 2024b)   ✗       Exp      High-level thought-templates.            Game, Reasoning, Coding
 SAGE (Liang et al., 2025)                 ✗       Exp      Dual-store with forgetting mechanism.    Game, Reasoning, Coding
 ChemAgent (Tang et al., 2025c)            ✗       Exp      Structured sub-tasks and principles.     Chemistry
 AgentKB (Tang et al., 2025d)              ✗       Exp      5-tuple experience nodes.                Coding, Reasoning
 H2 R (Ye et al., 2025b)                   ✗       Exp      Planning and Execution layers.           Game, Embodied Simula-
                                                                                                     tion
 AWM (Wang et al., 2024m)                  ✗       Exp      Abstracted universal workflows.          Web
 PRINCIPLES (Kim et al., 2025a)            ✗       Exp      Rule templates from self-play.           Emotional Companion
 ReasoningBank (Ouyang et al., 2025)       ✗       Exp      Transferable reasoning strategy items.   Web
 Voyager (Wang et al., 2024b)              ✔       Exp      Executable skill code library.           Game
 DGM (Zhang et al., 2025i)                 ✗       Exp      Recursive self-modifiable codebase.      Coding
 Memp (Fang et al., 2025d)                 ✗       Exp      Instructions and abstract scripts.       Embodied     Simulation,
                                                                                                     Travel Planning
 UFO2 (Zhang et al., 2025a)                ✔       Exp      System docs and interaction records.     Windows OS
 LEGOMem (Han et al., 2025a)               ✗       Exp      Vectorized task trajectories.            Office
 ToolMem (Xiao et al., 2025b)              ✗       Exp      Tool capability.                         Tool Calling
 SCM (Wang et al., 2025a)                  ✗       Fact     Memory stream and vector database.       Long-context
 MemoryBank (Zhong et al., 2024)           ✗       Fact     History and user profile.                Emotional Companion
 MPC (Lee et al., 2023)                    ✗       Fact     Persona and summary vector pool.         QA
 RecMind (Wang et al., 2024h)              ✗       Fact     User metadata and external knowledge.    Recommendation
 InteRecAgent (Huang et al., 2025d)        ✗       Fact     User profiles and candidate item.        Recommendation
 Ego-LLaVA (Shen et al., 2024)             ✔       Fact     Language-encoded chunk embeddings.       Multimodal QA
 ChatHaruhi (Li et al., 2023a)             ✗       Fact     Dialogue database from media.            Role-Playing
 Memochat (Lu et al., 2023)                ✗       Fact     Memos and categorized dialogue history.  Long-conv QA
 RecursiveSum (Wang et al., 2025h)         ✗       Fact     Recursive summaries of short dialogues.  Long-conv QA
 MemGPT (Packer et al., 2023a)             ✗       Fact     Virtual memory (Main/External contexts). Long-conv QA, Doc QA
                                                                                                        Continued on next page



                                                                15
Table 1 Comparison of representative token-level memory methods. We categorize existing works into three groups based
on their topological complexity: Flat Memory (1D) for linear or independent records, Planar Memory (2D) for structured
single-layer graphs/trees, and Hierarchical Memory (3D) for multi-level architectures. Methods are characterized across
four dimensions: (1) Multi indicates multimodal capability, where ✔ denotes support for modalities beyond text (e.g.,
visual) and ✗ implies text-only; (2) Type identifies the specific functional category of the memory (e.g., Fact for factual
memory, Exp for experiential memory, Work for working memory ); (3) Memory Structure details the organization
mechanism of the stored units; and (4) Task lists the primary application domains. (continued)

Method                                 Multi   Type               Memory Structure                  Task
RoleLLM (Wang et al., 2024d)           ✗       Fact   Role-specific QA pairs.                    Role-Playing
Think-in-memory (Liu et al., 2023a)    ✗       Fact   Hash table of inductive thoughts.          Long-conv QA
PLA (Yuan et al., 2025b)               ✗       Fact   Evolving records of history and summaries. QA, Human Feedback
COMEDY (Chen et al., 2025d)            ✗       Fact   Single-model compressed memory format. Summary, Compression,
                                                                                                 QA
Memoro (Zulfikar et al., 2024)         ✔       Fact   Speech-to-text vector embeddings.          User Study
Memory Sharing (Gao and Zhang,         ✗       Fact   Query-Response pair retrieval.             Literary Creation, Logic,
2024a)                                                                                           Plan Generation
Conv Agent(Alonso et al., 2024)        ✗       Fact   Chain-of-tables and vector entries.        QA
EM-LLM (Fountas et al., 2025)          ✗       Fact   Episodic events with Bayesian boundaries. Long-context
Memocrs (Xi et al., 2024a)             ✗       Fact   User metadata and knowledge.               Recommendation
SECOM (Pan et al., 2025)               ✗       Fact   Paragraph-level segmented blocks.          Long-conv QA
Mem0 (Chhikara et al., 2025)           ✗       Fact   Summary and original dialogue.             Long-conv QA
RMM (Tan et al., 2025c)                ✗       Fact   Reflection-organized flat entries.         Personalization
MEMENTO (Kwon et al., 2025)            ✔       Fact   Interaction history entries.               Personalization
MemGuide (Du et al., 2025b)            ✗       Fact   Dialogue-derived QA pairs.                 Long-conv QA
MIRIX (Wang and Chen, 2025)            ✔       Fact   Six optimized flat memory types.           Long-conv QA
SemanticAnchor (Chatterjee and Agar-   ✗       Fact   Syntactic 5-tuple structure.               Long-conv QA
wal, 2025)
MMS (Zhang et al., 2025b)              ✗       Fact   Dual Retrieval and Context units.             Long-conv QA
Memory-R1 (Yan et al., 2025c)          ✗       Fact   RL-managed mem0 architecture.                 Long-conv QA
ComoRAG (Wang et al., 2025f)           ✗       Fact   Fact/Semantic/Plot units with probes.         Narrative QA
Nemori (Nan et al., 2025)              ✗       Fact   Predictive calibration store.                 Long-conv QA
Livia (Xi and Wang, 2025)              ✔       Fact   Pruned interaction history.                   Emotional Companion
MOOM (Chen et al., 2025e)              ✗       Fact   Decoupled plot and character stores.          Role-Playing
Mem-α (Wang et al., 2025p)             ✗       Fact   Core, Semantic, and Episodic Mem.             Memory Management
Personalized Long term Interac-        ✗       Fact   Hierarchical history and summaries.           Personalization
tion (Westhäußer et al., 2025)
LightMem (Fang et al., 2025b)          ✗       Fact   Optimized Long/Short-term store.              Long-conv QA
MEXTRA (Wang et al., 2025b)            ✗       Fact   Extracted raw dialogue data.                  Privacy Attack
MovieChat (Song et al., 2024)          ✔       Fact   Short-term features and long-term persis-     Video Understanding
                                                      tence.
MA-LMM (He et al., 2024)               ✔       Fact   Visual and Query memory banks.                Video Understanding
VideoAgent (Wang et al., 2024g)        ✔       Fact   Temporal text descriptions and object         Video Understanding
                                                      tracking.
Video-RAG (Luo et al., 2025b)          ✔       Fact   Visually-aligned information .                Video Understanding
KARMA (Wang et al., 2025r)             ✔       Fact   3D scene graph and dynamic object states.     Embodied Task
Embodied VideoAgent (Fan et al.,       ✔       Fact   Persistent object and sensor store.           MultiModal
2025)
Mem2Ego (Zhang et al., 2025m)          ✔       Fact   Map, landmark, and visited location stores.   Embodied Navigation
Context-as-Memory (Yu et al., 2025b)   ✔       Fact   Generated context frames.                     Video Generation
RCR-Router (Liu et al., 2025d)         ✗       Fact   Budget-aware semantic subsets.                QA
ELL (Cai et al., 2025a)                ✗       Fact   Liflong memory and skills.                    Lifelong Learning
MemRL (Zhang et al., 2026)             ✗       Exp    RL for memory management.                     Web
ReMe (Cao et al., 2025b)               ✗       Exp    Step level experience and insight.            Web
MMAG (Zeppieri, 2025)                  ✗       Fact   Five interacting memory layers.               User Study
Hindsight (Latimer et al., 2025)       ✗       Fact   Retains, recalls, and reflects.               Long-conv QA
GAM (Yan et al., 2025a)                ✗       Fact   Simple memory but search is guided.           Long-conv QA
                                                 Planar Memory Models
D-SMART (Lei et al., 2025)             ✗       Fact   Structured memory with reasoning trees.       Long-conv QA
Reflexion (Shinn et al., 2023b)        ✗       Work   Reflective text buffer from experiences.      QA, Reasoning, Coding
                                                                                                     Continued on next page



                                                           16
Table 1 Comparison of representative token-level memory methods. We categorize existing works into three groups based
on their topological complexity: Flat Memory (1D) for linear or independent records, Planar Memory (2D) for structured
single-layer graphs/trees, and Hierarchical Memory (3D) for multi-level architectures. Methods are characterized across
four dimensions: (1) Multi indicates multimodal capability, where ✔ denotes support for modalities beyond text (e.g.,
visual) and ✗ implies text-only; (2) Type identifies the specific functional category of the memory (e.g., Fact for factual
memory, Exp for experiential memory, Work for working memory ); (3) Memory Structure details the organization
mechanism of the stored units; and (4) Task lists the primary application domains. (continued)

 Method                                 Multi   Type              Memory Structure                  Task
 PREMem (Kim et al., 2025b)             ✗       Fact   Dynamic cross-session linked triples.     Long-conv QA
 Query Reconstruct (Xu et al., 2025b)   ✗       Exp    Logic graphs built from knowledge bases. KnowledgeGraph QA
 KGT (Sun et al., 2024)                 ✗       Fact   KG node from query and feedback.          QA
 Optimus-1 (Li et al., 2024d)           ✔       F&E    Knowledge graph and experience pool.      Game
 SALI (Pan et al., 2024)                ✔       Exp    Topological graph with spatial nodes      Navigation
 HAT (A et al., 2024)                   ✗       Fact   Hierarchical aggregate tree.              Long-conv QA
 MemTree (Rezazadeh et al., 2025c)      ✗       Fact   Dynamic hierarchical conversation tree.   Long-conv QA
 TeaFarm (iunn Ong et al., 2025)        ✗       Fact   Causal edges connecting memories.         Long-conv QA
 COMET (Kim et al., 2024b)              ✗       Fact   Context-aware memory through graph.       Long-conv QA
 Intrinsic Memory (Yuen et al., 2025)   ✗       Fact   Private internal and shared external mem. Planning
 A-MEM (Xu et al., 2025c)               ✗       Fact   Card-based connected mem.                 Long-conv QA
 Ret-LLM (Modarressi et al., 2023)      ✗       Fact   Triplet table and LSH vectors.            QA
 HuaTuo (Wang et al., 2023a)            ✗       Fact   Medical Knowledge Graph.                  Medical QA
 M3-Agent (Long et al., 2025)           ✔       Fact   Multimodal nodes in graph structure.      Embodied QA
 EMem (Zhou and Han, 2025a)             ✗       Fact   Event-centric alternative with pagerank.  Long-conv QA
 WorldMM (Yeo et al., 2025)             ✔       Fact   Multiple complementary memories.          Video Understanding
 Memoria (Sarin et al., 2025)           ✗       Fact   Knowledge-graph profile and summary.      Long-conv QA
 LingoEDU (Zhou et al., 2026)           ✗       Fact   Relation tree of Elementary Discourse Long-conv QA
                                                       Units.
                                                Hierarchical Memory Models
 GraphRAG (Edge et al., 2025)           ✗       Fact   Multi-level community graph indices.     QA, Summarization
 H-Mem (Sun and Zeng, 2025)             ✗       Fact   Decoupled index layers and content layers.
                                                                                                Long-conv QA
 EMG-RAG (Wang et al., 2024l)           ✗       Fact   Three-tiered memory graph.               QA
 G-Memory (Zhang et al., 2025c)         ✗       Exp    Query-centric three-layer graph structure.
                                                                                                QA, Game, Embodied
                                                                                                Task
 Zep (Rasmussen et al., 2025)           ✗       Fact Temporal Knowledge Graphs.                 Long-conv QA
 SGMem (Wu et al., 2025h)               ✗       Fact Chunk Graph and Sentence Graph.            Long-conv QA
 HippoRAG (Gutierrez et al., 2024)      ✗       Fact Knowledge with query nodes.                QA
 HippoRAG 2 (Gutiérrez et al., 2025)    ✗       Fact KG with phrase and passage.                QA
 AriGraph (Anokhin et al., 2024)        ✗       Fact Semantic and Episodic memory graph.        Game
 Lyfe Agents (Kaiya et al., 2023)       ✗       Fact Working, Short & Long-term layers.         Social Simulation
 CAM (Li et al., 2025g)                 ✗       Fact Multilayer graph with topic.               Doc QA
 HiAgent (Hu et al., 2025a)             ✗       E&W Goal graphs with recursive cluster.         Agentic Tasks
 ILM-TR (Tang et al., 2024)             ✗       Fact Hierarchical Memory tree.                  Long-context
 CompassMem (Hu et al., 2026b)          ✗       Fact Hierarchical event-centric Memory.         QA
 MAGMA (Jiang et al., 2026)             ✗       Fact Semantic, temporal, causal, entity graphs. Long-conv QA
 EverMemOS (Hu et al., 2026a)           ✗       Fact Reusable memories covering multi types.    Long-conv QA
 RGMem (Tian et al., 2025a)             ✗       Fact Renormalization Group-based memory.        Long-conv QA
 MemVerse (Liu et al., 2025e)           ✔       Fact Multimodal hierarchical knowledge graphs. Reasoning, QA




Dialogue Some flat memory work focuses on storing and managing dialogue content. Early approaches
primarily focused on preventing forgetting by storing raw dialogue history or generating recursive summaries
to extend context windows (Wang et al., 2025a; Lu et al., 2023; Wang et al., 2025h; Yuan et al., 2025b).
MemGPT (Packer et al., 2023a) introduces an operating-system metaphor with hierarchical management,
inspiring subsequent works (Li et al., 2025l; Kang et al., 2025a) to decouple active context from external
storage for infinite context management.
To improve retrieval precision, the granularity and structure of memory units have become increasingly diverse


                                                            17
and cognitively aligned. Some works, like COMEDY (Chen et al., 2025d), Memory Sharing (Gao and Zhang,
2024a) and MemGuide (Du et al., 2025b) compress information into compact semantic representations or
query-response pairs to facilitate direct lookup, while others, like Alonso et al. (2024) and MIRIX (Wang and
Chen, 2025) adopt hybrid structures ranging from vector-table combinations to multi-functional memory types.
Furthermore, research has begun to define memory boundaries based on cognitive psychology, organizing
information through syntactic tuples (Chatterjee and Agarwal, 2025) or segmenting events based on Bayesian
surprise and paragraph structures (Fountas et al., 2025; Pan et al., 2025) , thereby matching human-like
cognitive segmentation.
As conversational depth increases, memory evolves to store high-level cognitive processes and narrative
complexities. Instead of mere factual records, systems like Think-in-Memory (Liu et al., 2023a) and RMM (Tan
et al., 2025c) store inductive thoughts and retrospective reflections to guide future reasoning. In complex
scenarios such as role-playing or long narratives, approaches like ComoRAG (Wang et al., 2025f) and
MOOM (Chen et al., 2025e) decompose memory into factual, plot-level, and character-level components,
ensuring the agent maintains a coherent persona and understanding across extended interactions.
Memory has transitioned from static storage to autonomous and adaptive optimization. Mem0(Chhikara
et al., 2025) established standardized operations for memory maintenance, laying the foundation for intelligent
control. Recent advances introduce reinforcement learning to optimize memory construction (Yan et al., 2025c;
Wang et al., 2025p), while other mechanisms focus on dynamic calibration and efficiency, such as predicting
missing information (Nan et al., 2025), managing token budgets across multi-agent systems (Liu et al., 2025d)
, and reducing redundancy in long-term storage (Fang et al., 2025b).

Preference Some memory systems focus on modeling a user’s evolving tastes, interests, and decision patterns,
especially in recommendation scenarios where preference understanding is central. Unlike dialogue-centric
memory, which focuses on maintaining conversational coherence, preference memory centers on identifying
a user’s tastes and tendencies. Early efforts such as RecMind (Wang et al., 2024h) separate user-specific
information from external domain knowledge by storing both factual user attributes and item metadata.
InteRecAgent (Huang et al., 2025d) folds memory into the recommendation workflow but focuses more on the
current candidate set, keeping user profiles and the active item pool to support context-aware recommendations.
MR.Rec (Huang et al., 2025b) builds a memory index archiving the full interaction process, storing raw item
information and per-category preference summaries. In conversational settings, Memocrs (Xi et al., 2024a)
proposes a more structured design with a user-specific memory tracking entities and user attitudes, and a
general memory aggregating cross-user knowledge.

Profile A subset of flat memory systems focuses on storing and maintaining stable user profiles, character
attributes, or long-term identity information so that agents can behave consistently across turns and tasks.
MemoryBank (Zhong et al., 2024) represents one of the earliest frameworks in this direction: it organizes
dialogue history and event summaries by timestamp, gradually building a user profile that supports accurate
retrieval of identity-relevant information. AI Persona (Wang et al., 2024f) makes the memory system process
information not only presented in the dialogue context but also from multi-dimensional human-AI interaction
dimensions. MPC (Lee et al., 2023) extends this idea by storing real-time persona information and dialogue
summaries in a memory pool, keeping conversation behavior aligned with a consistent persona over long
interactions. Westhäußer et al. (2025) proposes a more comprehensive profile-maintenance mechanism,
combining long-term and short-term memory with automatically generated summaries after each turn to form
a mid-term context, allowing the user profile to evolve continuously through interaction.
In virtual role-playing settings, ChatHaruhi (Li et al., 2023a) extracts dialogue from novels and television
scripts, enabling the model to maintain character-consistent behavior by retrieving memory. RoleLLM (Wang
et al., 2024d) takes a more structured approach by building question–answer pairs to capture character-specific
knowledge.

Experience Distinct from the static, general knowledge, experience memory stems from the agent’s dynamic
accumulation during actual interaction tasks, encompassing specific observations, chains of thought, action
trajectories, and environmental feedback. It is important to note that this section just provides a brief



                                                      18
overview of experiential memory strictly from the perspective of token-level storage; a more comprehensive
analysis and detailed discussion of this domain will be presented in Section 4.2.
The most fundamental form of experience memory involves the direct archival of historical behavioral
trajectories. This paradigm enables agents to inform current decision-making by retrieving and reusing past
instances, encompassing both successful and failed cases (Zhou et al., 2025a; Wang et al., 2025q).
To address the limited generalizability inherent in raw trajectories, a significant body of research focuses on
abstracting specific interactions into higher-level, generalized experiences. As one of the earliest and most
influential approaches, Reflexion (Shinn et al., 2023b) distinguishes short-term memory as the trajectory
history and long-term memory as the feedback produced by the self-reflection model. Certain studies compress
complex interaction histories into universal workflows, rule templates, or high-level “thought-templates” to
facilitate cross-problem transfer and reuse (Wang et al., 2024m; Kim et al., 2025a; Yang et al., 2024b). Other
works emphasize the structural organization and dynamic maintenance of memory. These approaches ensure
that stored insights remain adaptable to novel tasks and are efficiently updated by constructing domain-specific
structured knowledge bases, employing hierarchical plan-execute memory architectures, or incorporating
human-like forgetting and reflection mechanisms (Tang et al., 2025c,d; Ouyang et al., 2025; Ye et al., 2025b;
Zhao et al., 2024; Liang et al., 2025).
In contexts involving programming or specific tool utilization, experience memory evolves into executable
skills. Within this paradigm, agents consolidate exploration experiences into code repositories, procedural
scripts, or tool-usage entries. Leveraging environmental feedback, these systems iteratively refine code quality
or even dynamically modify their underlying logic to achieve self-evolution (Wang et al., 2024a; Yin et al.,
2025; Fang et al., 2025d; Xiao et al., 2025b). Furthermore, targeting complex environments such as operating
systems, some studies distill successful execution records into reusable exemplars or vectorized representations,
thereby facilitating an efficient pipeline from offline construction to online allocation (Zhang et al., 2025a;
Han et al., 2025a).

Multimodal Multimodal memory systems store information in the form of discrete token-level units
extracted from raw multimodal data, such as images, video frames, audio segments, and text, enabling agents
to capture, compress, and retrieve knowledge across channels and over long spans of experience. In wearable
and egocentric settings, early work such as Ego-LLaVA (Shen et al., 2024) captures first-person video and
converts it into lightweight language descriptions. Memoro (Zulfikar et al., 2024) follows a similar philosophy
but uses speech-to-text to form embedding-based memory chunks. Building on this direction, Livia (Xi and
Wang, 2025) incorporates long-term user memory into an AR system with emotional awareness, applying
forgetting curves and pruning strategies.
For video understanding, the emphasis shifts toward separating transient visual cues from enduring contextual
information. MovieChat (Song et al., 2024) adopts a short-term/long-term split, storing recent frame features.
MA-LMM (He et al., 2024) pushes this further with a dual-bank design—one storing raw visual features and
the other retaining query embeddings. VideoAgent (Wang et al., 2024g) adopts a more semantically organized
approach, maintaining a temporal memory of textual clip descriptions alongside object-level memory that
tracks entities across frames. In interactive video generation, Context-as-Memory (Yu et al., 2025b) shows
that simply storing previously generated frames as memory can also be highly effective. WorldMM (Yeo et al.,
2025) constructs multiple mutually reinforcing memory modules that capture information in both textual and
visual modalities.
In embodied scenarios, memory becomes inherently tied to spatial structure and ongoing interaction.
KARMA (Wang et al., 2025r) introduces a two-tier memory system: long-term memory stores static objects
in a 3D scene graph, while short-term memory tracks object positions and state changes. Embodied VideoA-
gent (Fan et al., 2025) also builds persistent object memories but fuses them with first-person video and
additional embodied sensors. Mem2Ego (Zhang et al., 2025m) extends this idea to navigation by separating
global maps, landmark descriptions, and visitation histories into three distinct memory stores. Complementing
these task-driven designs, MEMENTO (Kwon et al., 2025) provides an evaluation framework that treats
multimodal interaction history as an agent’s memory, enabling systematic assessment of how well embodied
systems utilize accumulated perceptual experience.



                                                       19
Discussion The primary advantage of Flat Memory is their simplicity and scalability: memory can be
appended or pruned with minimal cost, and retrieval methods such as similarity search allow flexible access
without requiring predefined structure. This makes them suitable for broad recall, episodic accumulation,
and rapidly changing interaction histories. However, the lack of explicit relational organization means that
coherence and relevance depend heavily on retrieval quality. As the memory grows, redundancy and noise
can accumulate, and the model may retrieve relevant units without understanding how they relate, limiting
compositional reasoning, long-horizon planning, and abstraction formation. Thus, topology-free collections
excel at broad coverage and lightweight updates, but are constrained in tasks requiring structured inference
or stable knowledge organization.

3.1.2   Planar Memory (2D)


  Definition of Planar (2D) Memory

  Planar Memory introduces an explicit organizational topology among memory units, but only within
  a single structural layer, which for short called 2D. The topology may be a graph, tree, table, implicit
  connection structure and so on, where relationships such as adjacency, parent–child ordering, or semantic
  grouping are encoded within one plane, without hierarchical levels or cross-layer references.

The core of Planar memory forms lies in breaking through a single storage pool by establishing explicit
association mechanisms, achieving a leap from mere “storage” to “organization”.

Tree Tree structures organize information hierarchically and can handle different levels of abstraction.
HAT (A et al., 2024) builds a Hierarchical Aggregate Tree by segmenting long interactions and then aggregating
them step by step. This multi-level structure supports coarse-to-fine retrieval and performs better than flat
vector indices in long-context question answering. To reduce dialogue fragmentation, MemTree (Rezazadeh
et al., 2025c) introduces a dynamic representation that infers hierarchical schemas from isolated conversation
logs. It gradually summarizes concrete events into higher-level concepts, allowing agents to use both detailed
memories and abstract knowledge.

Graph Graph structures dominate the landscape of 2D memory due to their ability to capture complex
associations, causality, and temporal dynamics. Foundational works like Ret-LLM (Modarressi et al., 2023)
abstract external storage into addressable triple-based units, enabling the LLM to interact with a relation-
centric table that functions like a lightweight knowledge graph. In the medical domain, HuaTuo (Wang et al.,
2023a) injects professional knowledge by integrating a structured corpus of Chinese medical knowledge graphs
and clinical texts to fine-tune the base model. KGT (Sun et al., 2024) introduces a real-time personalization
mechanism where user preferences and feedback are encoded as nodes and edges in a user-specific knowledge
graph. For reasoning-intensive tasks, PREMem (Kim et al., 2025b) shifts part of the inference burden to
the memory construction phase, deriving structured memory items and their evolution relations from raw
dialogue. Similarly, Memory-augmented Query Reconstruction (Xu et al., 2025b) maintains a dedicated query
memory that records past KG queries and reasoning steps, using retrieved records to reconstruct more accurate
queries. Building on a timeline perspective, TeaFarm (iunn Ong et al., 2025) organizes dialogue history along
segmented timelines and applies structured compression to manage lifelong context. COMET (Kim et al.,
2024b) further refines conversational memory by using external commonsense bases to parse dialogue and
dynamically update a context-aware persona graph with inferred hidden attributes. A-Mem (Xu et al., 2025c)
standardizes knowledge into card-like units. It organizes them by relevance and places related memories
in the same box, which builds a complete memory network. Intrinsic Memory Agents (Yuen et al., 2025)
employ a partitioned architecture in which sub-agents maintain their own role-specific private memories while
collaboratively reading and writing to a shared memory. Extending to multimodel agents, M3-Agent (Long
et al., 2025) unifies image, audio, and text into an entity-centric memory graph. SALI (Pan et al., 2024)
constructs a Reality–Imagination Hybrid Memory, unifying real observations and imagined future scenarios
into a consistent navigation graph.




                                                     20
Hybrid Complex tasks often require hybrid architectures that segregate distinct cognitive functions while
sharing a common memory substrate. Optimus-1 (Li et al., 2024d) explicitly separates static knowledge into
a hierarchical directed knowledge graph for planning, and dynamic interactions into an abstract multimodal
experience Pool for reflection and self-improvement. D-SMART (Lei et al., 2025) combines a structured
factual memory, implemented as a continuously updated knowledge graph, with a traversal-based reasoning
tree.

Discussion The Planar Memory, by effectively establishing links between its nodes, enables memories
to leverage collective synergies and thus encode more comprehensive contextual knowledge. Moreover, it
supports retrieval mechanisms that go beyond simple iteration, including structured key–value lookups and
relational traversal along graph edges. These capabilities make the form strong in storing, organizing, and
managing memories. However, it also faces a critical limitation: Without a hierarchical storage mechanism,
all memories must be consolidated into a single, monolithic module. As task scenarios grow in complexity and
diversity, this redundant and flattened design becomes increasingly inadequate for robust performance. More
importantly, the high construction and search costs significantly hinder its practical deployment.

3.1.3   Hierarchical Memory (3D)


  Definition of Hierarchical (3D) Memory

  Hierarchical memory organizes information across layers, using inter-level connections to shape the
  memories into a volumetric structured space.

Such hierarchies support representations at different degrees of abstraction—from raw observations, to compact
event summaries, to higher-level thematic patterns. Cross-layer connections further yield a volumetric memory
space through which the system can navigate not only laterally among units but also vertically across
abstraction levels.
Hierarchical Memory moves beyond simple stratification, aiming to build complex systems with deep abstraction
capabilities and dynamic evolutionary mechanisms. These works typically employ multi-level graph structures
or neuroscience-inspired mechanisms to build a more human-like volumetric memory space, where information
is richer and the connections between memory units are clearer and more explicit.

Pyramid This category constructs memory as multi-level pyramids, where information is progressively
organized into higher layers of abstraction and queried in a coarse-to-fine manner. HiAgent (Hu et al.,
2025a) manages long-horizon tasks through a subgoal-centered hierarchical working memory, keeping detailed
trajectories for the currently active subgoal while compressing completed subgoals into higher-level summaries
that can be selectively retrieved when needed. GraphRAG (Edge et al., 2025) builds a multi-level graph index
via community detection, recursively aggregating entity-level subgraphs into community-level summaries.
Extending the idea of clustering memory nodes, Zep (Rasmussen et al., 2025) formalizes agent memory as a
Temporal Knowledge Graph, and it similarly performs community partitioning. ILM-TR (Tang et al., 2024)
employs a tree-structured, pyramidal index coupled with an Inner Loop mechanism, repeatedly querying
summaries at different abstraction levels and updating a short-term memory buffer until the retrieved evidence
and generated answer stabilize. To ensure controllable personalization, EMG-RAG (Wang et al., 2024l)
organizes an Editable Memory Graph into three tiers, where a tree-like type and subclass index (L1, L2)
sits above an entity-level memory graph (L3). In multi-agent systems, G-Memory (Zhang et al., 2025c)
structures shared experience using a three-tier graph hierarchy of insight, query, and interaction graphs. This
design enables query-centric traversal to move vertically between high-level cross-trial insights and compact
trajectories of concrete collaborations.

Multi-Layer These forms instead emphasize layered specialization, organizing memory into distinct modules
or levels that focus on particular information types or functions. Lyfe Agents (Kaiya et al., 2023) separates
salient long-term records from low-value transient details, allowing the system to maintain a compact,
behaviorally important layer of memories. H-Mem (Sun and Zeng, 2025) explicitly arranges long-term


                                                      21
dialogue memory into a multi-level hierarchy ordered by semantic abstraction, where lower layers store
fine-grained interaction snippets and higher layers store increasingly compressed summaries. Biologically
inspired architectures such as HippoRAG (Gutierrez et al., 2024) factor memory into an associative indexing
component, implemented as an open knowledge graph, and an underlying passage store, using the graph
layer to orchestrate multi-hop retrieval over stored content. Its successor, HippoRAG 2 (Gutiérrez et al.,
2025), extends this design into a non-parametric continual-learning setting, enriching the indexing layer with
deeper passage integration and online LLM filtering. AriGraph (Anokhin et al., 2024) separates memory by
information type within a unified graph, combining a semantic knowledge-graph world model that encodes
environment structure with an event-level component that links concrete observations back to the semantic
backbone. Similarly, SGMem (Wu et al., 2025h) adds a sentence-graph memory level on top of raw dialogue,
representing histories as sentence-level graphs within chunked units. CAM (Li et al., 2025g) layers the reading
process itself by incrementally clustering overlapping semantic graphs into a hierarchical schemata structure.
Recently, methods such as CompassMem (Hu et al., 2026b) and MAGMA (Jiang et al., 2026) have begun
exploring hierarchical composition strategies enriched with logical relations, aiming to make memory retrieval
and utilization more efficient and comprehensive, so that memory can provide models with benefits beyond
mere semantic information.

Discussion By placing memory nodes at the intersection of hierarchical and relational dimensions, Hier-
archical Memory allows different memories to interact and form multi-dimensional synergies. This design
helps the system encode knowledge that is more holistic and more deeply contextualized. The form also
supports powerful retrieval: it enables complex, multi-path queries that move through relational networks
within each layer and across abstraction levels between layers. This ability allows the system to retrieve
task-relevant memories with high precision, leading to strong task performance. However, the structure’s
complexity and its dense information organization create challenges for both retrieval efficiency and overall
effectiveness. In particular, ensuring that all stored memories remain semantically meaningful and designing
the optimal three-dimensional layout of the system remain difficult and critical problems.

3.2      Parametric Memory
In contrast to token-level memory, which stores information as visible and editable discrete units, parametric
memory stores information directly in the model’s parameters. In this section, we examine methods that
embed memory into learnable parameter spaces, allowing the model to internalize and recall information
without referring to external storage.
Based on where the memory is stored relative to the core model parameters, we distinguish two primary forms
of parametric memory:

  Two Major Types of Parametric Memory

        1. Internal Parametric Memory: Memory encoded within the original parameters of the model (e.g.,
           weights, biases). These methods directly adjust the base model to incorporate new knowledge or
           behavior.
        2. External Parametric Memory: Memory stored in additional or auxiliary parameter sets, such as
           adapters, LoRA modules, or lightweight proxy models. These methods introduce new parameters
           to carry memory without modifying the original model weights.

This distinction reflects a key design choice: whether memory is fully absorbed into the base model or attached
modularly alongside it. In the subsections that follow, for each form we outline the implementation methods,
analyze its strengths and limitations, and list representative systems or work. Table 2 provides an overview of
representative parametric memory methods.

3.2.1    Internal Parametric Memory

Internal parameter memory injects domain knowledge, personalized knowledge, or priors required by down-
stream tasks into the model. We also regard enhancing the model’s long-context capability as injecting a prior.


                                                      22
Table 2 Taxonomy of parametric memory methods. We categorize existing works based on the storage location relative
to the core model: Internal Parametric Memory embeds knowledge directly into the original weights, while External
Parametric Memory isolates information within auxiliary parameter sets. Based on the training phase, we performed
a secondary classification of the articles. Methods are compared across three technical dimensions: (1) Type defines
the nature of the memory, (2) Task specifies the target downstream application, and (3) Optimization denotes the
optimization strategy, such as SFT, FT (fine-tuning) , and PE (prompt engineering).

 Method                                     Type            Task                                     Optimization
                                         I. Internal Parametric Memory
 (a) Pre-Train Phase
 TNL (Qin et al., 2024b)                    Working         QA, Reasoning                            SFT
 StreamingLLM (Xiao et al., 2024)           Working         QA, Reasoning                            SFT
 LMLM (Zhao et al., 2025b)                  Factual         QA, Factual Gen                          SFT
 HierMemLM (Pouransari et al., 2025)        Factual         QA, Language Modeling                    SFT
 Function Token (Zhang et al., 2025o)       Factual         Language Modeling                        Pretrain
 (b) Mid-Train Phase
 Agent-Founder (Su et al., 2025)        Experiential Tool Calling, Deep Research        SFT
 Early Experience (Zhang et al., 2025k) Experiential Tool Calling, Embodied Simulation, SFT
                                                     Reasoning, Web
 (c) Post-Train Phase
 Character-LM (Shao et al., 2023)           Factual         Role Playing                             SFT
 CharacterGLM (Zhou et al., 2024a)          Factual         Role Playing                             SFT
 SELF-PARAM (Wang et al., 2025o)            Factual         QA, Recommendation                       KL Tuning
 Room (Kim et al., 2023b)                   Experiential    Embodied Task                            RL
 KnowledgeEditor (Cao et al., 2021)         Factual         QA, Fact Checking                        FT
 Mend (Mitchell et al., 2022)               Factual         QA, Fact Checking, Model Editing         FT
 PersonalityEdit Mao et al. (2024)          Factual         QA, Model Editing                        FT, PE
 APP (Ma et al., 2024)                      Factual         QA                                       FT
 DINM (Wang et al., 2024c)                  Experiential    QA, Detoxification                       FT
 AlphaEdit (Fang et al., 2025c)             Factual         QA                                       FT
                                         II. External Parametric Memory
 (a) Adapter-based Modules
 MLP-Memory (Wei et al., 2025d)             Factual         QA, Classification, Textual Entailment   SFT
 K-Adapter (Wang et al., 2021)              Factual         QA, Entity Typing, Classification        SFT
 WISE (Wang et al., 2024e)                  Factual         QA, Hallucination Detection              SFT
 ELDER (Li et al., 2025d)                   Factual         Model Editing                            SFT
 T-Patcher (Huang et al., 2023)             Factual         QA                                       FT
 Sparse Memory FT (Lin et al., 2025a)       Factual         QA                                       SFT
 Memory Decoder (Cao et al., 2025a)         Factual         QA, Language Modeling                    SFT
 MemLoRA (Bini et al., 2025)                Factual         QA                                       SFT
 (b) Auxiliary LM-based Modules
 MAC (Tack et al., 2024)                    Factual      QA                                          SFT
 Retroformer (Yao et al., 2024a)            Experiential QA, Web Navigation                          RL


The timing of memory injection can be the pre-training phase, continued pre-training phase, mid-training
phase, or post-training phase. The memory stored in internal parameters does not add extra parameters or
additional modules.




                                                           23
Pre-Train Some works introduce memory mechanisms during the pre-training phase, aiming to address the
issue that long-tail world knowledge is difficult to compress into the limited model parameters. LMLM (Zhao
et al., 2025b) and HierMemLM (Pouransari et al., 2025) store the memory for knowledge retrieval in the model
during the pre-training phase, while storing the knowledge itself in an external knowledge base. Some works
also optimize the computational efficiency of attention to enhance long-window memory capability (Xiao
et al., 2024; Qin et al., 2024b,c; Dao, 2024; Shah et al., 2024).

Mid-Train During the continued pre-training phase, some works incorporate generalizable experience from
downstream tasks. For instance, Su et al. (2025) and Zhang et al. (2025k) integrate agent experience. Some
works improve the long-window performance or efficiency of LLMs during the mid-training phase, enabling
the model to maintain more short-term memory with longer windows in memory-aided tasks (Zaheer et al.,
2020; Chen et al., 2024a).

Post-Train Other works incorporate memory during the post-training phase to adapt to downstream
tasks. Some works enable LLMs to memorize personalized user history or styles. Some works allow LLMs
to learn from the successes or failures of past similar task executions. Character-LM (Shao et al., 2023)
and CharacterGLM (Zhou et al., 2024a) fine-tunes the LLM into different characteristics. During the post-
training phase, SELF-PARAM (Wang et al., 2025o) injects additional knowledge through KL divergence
distillation without requiring extra parameters. Room (Kim et al., 2023b) stores knowledge externally while
save experience internally. KnowledgeEditor (Cao et al., 2021) modifies internal parameters, aiming to alter
only the knowledge that requires editing. MEND (Mitchell et al., 2022) achieves fast knowledge editing by
using small networks to modify the gradients of large models. PersonalityEdit (Mao et al., 2024) proposes an
LLM personality editing dataset based on personality theories in psychology. APP (Ma et al., 2024) employs
multiple training objectives to ensure that adjacent knowledge is minimally disturbed during knowledge
editing. DINM (Wang et al., 2024c) proposes a model editing method that enables the model to learn to
reject such dangerous requests without affecting its normal functions.

Discussion The advantages of internal parameters lie in their simple structure, which does not add extra
inference overhead or deployment costs to the vanilla model. Their drawback is the difficulty in updating
internal parameters: storing new memory requires retraining, which is costly and prone to forgetting old
memory. Therefore, internal parameter memory is more suitable for large-scale storage of domain knowledge
or task priors, rather than short segments of personalized memory or working memory.

3.2.2   External Parametric Memory

Storing memory as tokens outside LLMs leads to insufficient understanding of token-form memory content in
the input window by the model. Meanwhile, storing memory in the parameters of LLMs has issues, such as
difficulty in updating and conflicts with pre-trained knowledge. Some works adopt a compromise approach,
which introduces memory through external parameters without altering the original parameters of LLMs.

Adapter A common line of external parametric memory methods relies on modules that are attached to a
frozen base model. MLP-Memory (Wei et al., 2025d) integrates RAG knowledge with Transformer decoders
through MLP. K-Adapter (Wang et al., 2021) injects new knowledge by training task-specific adapter modules
while keeping the original backbone unchanged, enabling continual knowledge expansion without interfering
with pre-trained representations. WISE (Wang et al., 2024e) further introduces a dual-parameter memory
setup—separating pre-trained knowledge and edited knowledge—and a routing mechanism that dynamically
selects which parameter memory to use at inference time, thus mitigating conflicts during lifelong editing.
ELDER (Li et al., 2025d) advances this direction by maintaining multiple LoRA modules and learning a
routing function that adaptively selects or blends them based on input semantics, improving robustness
and scalability in long-term editing scenarios. Collectively, these methods leverage additional parameter
subspaces to store and retrieve memory in a modular and reversible manner, avoiding the risks of catastrophic
interference associated with directly modifying the core model weights.




                                                     24
                             (a) Generate
                                      Auxiliary Models                     Latent Emb.
                                      SLM, LoRA,
                                      Decoder heads

                                               LLM Internal                        Interfere /
                                                Calculation                        augment




                                                    Inspection
                                                      Closer
                Input
                Query                    LLM                             Layer-wise               Output
                                       Forward                          transformer
                                                                          forward
                              KV cache/
                              Intermediate                       t
                                                             en
                              Embeddings              gm
                                                    au




                                                                      Token Token Token
                                                                     Selection Merge Projection
                              (b) Resue                                      (c) Transform

Figure 4 Overview of Latent Memory integration in LLM agents. Unlike explicit text storage, latent memory operates
within the model’s internal representational space. The framework is categorized by the origin of the latent state:
(a) Generate, where auxiliary models synthesize embeddings to interfere with or augment the LLM’s forward pass;
(b) Reuse, which directly propagates prior computational states such as KV caches or intermediate embeddings; and
(c) Transform, which compresses internal states through token selection, merging, or projection to maintain efficient
context.


Auxiliary LM Beyond Adapter-based storage, another line of work adopts a more architecturally decoupled
form of external parametric memory, where memory is stored in a separate model or external knowledge
module. MAC (Tack et al., 2024) compresses the information from a new document into a compact modulation
through an amortization network, and stores it in a memory bank. Retroformer (Yao et al., 2024a) proposes a
learning paradigm for memorizing the experiences of successes or failures in past task executions.

Discussion This external parametric memory approach provides a balance between adaptability and model
stability. Because memory is encoded into additional parameter modules, it can be added, removed, or
replaced without interfering with the base model’s pre-trained representation space. This supports modular
updates, task-specific personalization, and controlled rollback, while avoiding the catastrophic forgetting or
global weight distortion that may occur in full model fine-tuning.
However, this approach also comes with limitations. External parameter modules must still integrate with
the model’s internal representation flow, meaning that their influence is indirect and mediated through the
model’s attention and computation pathways. As a result, the effectiveness of memory injection depends on
how well the external parameters can interface with internal parametric knowledge.




                                                             25
3.3      Latent Memory

  Definition of Latent Memory

  Latent memory refers to memory that is carried implicitly in the model’s internal representations (e.g., KV
  cache, activations, hidden states, latent embeddings), rather than being stored as explicit, human-readable
  tokens or dedicated parameter sets.

Latent avoids exposing memory in plaintext and introduces practically less inference latency, while potentially
offering better performance gains by preserving fine-grained contextual signals within the model’s own
representational space.
As shown in Figure 4, we organize prior work by the origin of latent memory, which means how the latent
state is formed and introduced into the agent. We summarize the works in this part in Table 3.

  Three Major Types of Latent Memory

        1. Generate: latent memory is produced by an independent model or a module, and then supplied to
           the agent as reusable internal representations.
        2. Reuse: latent memory is directly carried over from prior computation, most prominently KV-cache
           reuse (within or across turns), as well as recurrent or stateful controllers that propagate hidden
           states.
        3. Transform: existing latent state is transformed into new representations(e.g., distillation, pooling,
           or compression), so the agent can retain essentials while reducing latency and context footprint.


3.3.1    Generate

A major line of work builds memory by generating new latent representations rather than reusing or transforming
existing activations. In this paradigm, the model or an auxiliary encoder creates compact continuous states.
These states may appear as special tokens in the sequence or as standalone vectors. They summarize the
essential information from long contexts, task trajectories, or multimodal inputs. The generated latent
summaries are then stored, inserted, or used as conditions for later reasoning or decision-making. This enables
the system to operate beyond its native context length, maintain task-specific intermediate states, and retain
knowledge across episodes without revisiting the original input. Although the concrete forms vary across
studies, the underlying idea remains consistent. Memory is explicitly produced through learned encoding or
compression, and the resulting latent states serve as reusable memory units that support future inference.
This design choice may also raise potential ambiguity with parametric memory, particularly since many
methods rely on separately trained models to generate latent representations. In this chapter, however, our
classification is grounded in the form of memory rather than the learning mechanism. Crucially, although these
approaches generate memory through learned encoding, the produced latent representations are explicitly
instantiated and reused as independent memory units, rather than being directly embedded into the model’s
parameters or forward-pass activations. We will return to this distinction when discussing individual methods
in detail.

Single Modal In the single-modal setting, a major group of methods focuses on long-context processing and
language modeling, where models generate a small set of internal representations to replace long raw inputs
(Mu et al., 2023; Luo et al., 2024; Xu et al., 2025d; Chevalier et al., 2023; Qian et al., 2025; Wang et al., 2024j,
2025n). A typical strategy is to compress long sequences into a few internal tokens or continuous vectors that
can be reused during later inference. For example, Gist (Mu et al., 2023) train a language model to produce
a set of gist tokens after processing a long prompt. Luo et al. (2024) introduce a special sentinel token at
each chunk boundary and encourage the model to aggregate local semantics into that token. SoftCoT (Xu
et al., 2025d) follows a similar direction by generating instance-specific soft tokens from the last hidden state.



                                                         26
Table 3 Taxonomy of latent memory methods. We categorize existing works based on the origin of the latent state:
Generate synthesizes memory via auxiliary modules, Reuse propagates internal computational states, and Transform
compresses, modifies or restructs existing latent state. Methods are compared across three tech
