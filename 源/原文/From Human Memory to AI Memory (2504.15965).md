---
source_url: https://arxiv.org/abs/2504.15965
source: arXiv 2504.15965
type: raw
created: 2026-07-06
tags: [学术论文, Agent记忆, raw]
---

# From Human Memory to AI Memory (2504.15965)

> 原始来源: https://arxiv.org/abs/2504.15965
> 入库日期: 2026-07-06
> 提取方式: ar5iv HTML → 纯文本提取

From Human Memory to AI Memory: A Survey on Memory Mechanisms in the Era of LLMs 

 Yaxiong Wu, Sheng Liang, Chen Zhang, Yichao Wang, Yongyue Zhang, 
 Huifeng Guo, Ruiming Tang, Yong Liu 
 Huawei Noah’s Ark Lab 
 wu.yaxiong@huawei.com 

 Abstract 
 Memory is the process of encoding, storing, and retrieving information, allowing humans to retain experiences, knowledge, skills, and facts over time, and serving as the foundation for growth and effective interaction with the world. It plays a crucial role in shaping our identity, making decisions, learning from past experiences, building relationships, and adapting to changes. In the era of large language models (LLMs), memory refers to the ability of an AI system to retain, recall, and use information from past interactions to improve future responses and interactions. Although previous research and reviews have provided detailed descriptions of memory mechanisms, there is still a lack of a systematic review that summarizes and analyzes the relationship between the memory of LLM-driven AI systems and human memory, as well as how we can be inspired by human memory to construct more powerful memory systems. To achieve this, in this paper, we propose a comprehensive survey on the memory of LLM-driven AI systems. In particular, we first conduct a detailed analysis of the categories of human memory and relate them to the memory of AI systems. Second, we systematically organize existing memory-related work and propose a categorization method based on three dimensions (object, form, and time) and eight quadrants. Finally, we illustrate some open problems regarding the memory of current AI systems and outline possible future directions for memory in the era of large language models. 

 1 Introduction 

 Recently, large language models (LLMs) have become the core component of AI systems due to their powerful language understanding and generation capabilities, and are widely used in various applications such as intelligent customer service, automated writing, machine translation, information retrieval, and sentiment analysis  [ 1 , 2 , 3 , 4 ] .
Unlike traditional AI systems, which rely on predefined rules and manually labeled features, LLM-driven AI systems offer greater flexibility, handling a diverse range of tasks with enhanced adaptability and contextual awareness.
Moreover, the introduction of memory enables LLMs to retain historical interactions with users and store contextual information, thereby providing more personalized, continuous, and context-aware responses in future interactions  [ 2 , 5 , 6 ] .
AI systems powered by LLMs with memory capabilities will not only elevate the user experience but also support more complex and dynamic use cases, steering AI technology toward greater intelligence and human-centric design  [ 7 , 8 ] . 

 In neuroscience, human memory refers to the brain’s ability to store, retain, and recall information  [ 9 , 10 ] .
Human memory serves as the foundation for understanding the world, learning new knowledge, adapting to the environment, and making decisions, allowing us to preserve past experiences, skills, and knowledge, and helping us form our personal identity and behavior patterns  [ 11 ] .
Human memory can be broadly classified into short-term memory and long-term memory based on the duration of new memory formation  [ 12 ] .
Short-term memory refers to the information we temporarily store and process, typically lasting from a few seconds to a few minutes, and includes sensory memory and working memory  [ 11 ] .
Long-term memory refers to the information we can store for extended periods, ranging from minutes to years, and includes declarative explicit memory (such as episodic and semantic memory) and non-declarative implicit memory (such as conditioned reflexes and procedural memory)  [ 11 ] .
Human memory is a complex and dynamic process that relies on different memory systems to process information for various purposes, influencing how we understand and respond to the world.
The different types of human memory and their working mechanisms can greatly inspire us to develop more scientific and reasonable memory-enhanced AI systems  [ 13 , 14 , 15 , 16 ] . 

 In the era of large language models (LLMs), the most typical memory-enhanced AI system is the LLM-powered autonomous agent system  [ 10 ] .
Large language model (LLM) powered agents are AI systems that can perform complex tasks using natural language, incorporating capabilities like planning, tool use, memory, and multi-step reasoning to enhance interactions and problem-solving  [ 1 , 2 , 10 ] .
This memory-enhanced AI system is capable of autonomously decomposing complex tasks, remembering interaction history, and invoking and executing tools, thereby efficiently completing a series of intricate tasks.
In particular, memory, as a key component of the LLM-powered agent, can be defined as the process of acquiring, storing, retaining, and subsequently retrieving information  [ 10 ] .
It enables the large language model to overcome the limitation of LLM’s context window, allowing the agent to recall interaction history and make more accurate and intelligent decisions.
For instance, MemoryBank  [ 17 ] proposed a long-term memory mechanism to allow LLMs for retrieving relevant memories, continuously evolving through continuous updates, and understanding and adapting to a user’s personality by integrating information from previous interactions.
In addition, many commercial and open-source AI systems have also integrated memory systems to enhance the personalization capabilities of the system, such as OpenAI ChatGPT Memory  [ 18 ] , Apple Personal Context  [ 19 ] , mem0  [ 20 ] , MemoryScope  [ 21 ] , etc. 

 Although previous studies and reviews have provided detailed explanations of memory mechanisms, most of the existing work focuses on analyzing and explaining memory from the temporal (time) dimension, specifically in terms of short-term and long-term memory  [ 8 , 7 , 17 ] .
We believe that categorizing memory solely based on the time dimension is insufficient, as there are many other aspects (such as object and form ) to memory classification in AI systems.
For example, from the object dimension, since AI systems often interact with humans, they need to perceive, store, recall, and use memories related to individual users, thus generating personal memories. Meanwhile, when AI systems perform complex tasks, they generate intermediate results (such as reasoning and planning processes, internet search results, etc.), which form system memory.
In addition, from the form dimension, since AI systems are powered by large language models (LLMs), they can store memories through the parametric memory encoded within the model parameters, as well as through non-parametric memory in the form of external memory documents that are stored and managed outside the model.
Therefore, insights that consider memory from the perspectives of object (personal and system), form (parametric and non-parametric), and time (short-term and long-term) are still lacking in the current era of large language models.
There is still no comprehensive review that systematically analyzes the relationship between memory in LLM-driven AI systems and human memory, and how insights from human memory can be leveraged to build more efficient and powerful memory systems. 

 To fill this gap, this paper presents a comprehensive review of the memory mechanisms in LLM-driven AI systems.
First, we provide a detailed analysis of the categories of human memory and relate them to the memory systems in AI.
In particular, we explore how human memory types — short-term memory (including sensory memory and working memory) and long-term memory (including explicit memory and implicit memory) — correspond to personal and system memory, parametric and non-parametric memory, and short-term and long-term memory in LLM-driven AI systems.
Next, we systematically organize the existing work related to memory and propose a classification method based on three dimensions ( object , form , and time ) with eight quadrants.
In the object dimension, memory can be divided into personal memory and system memory; in the form dimension, it can be classified into parametric memory and non-parametric memory; in the time dimension, memory can be categorized into short-term memory and long-term memory.
Finally, based on the classification results from the three dimensions and eight quadrants mentioned above, we analyze some open issues in the memory of current AI systems and outline potential future directions for memory development in the era of large language models. 

 The main contributions of this paper are summarized as follows:
(1) We systematically and comprehensively define LLM-driven AI systems’ memory and establish corresponding relationships with human memory.
(2) We propose a classification method for memory based on three dimensions (object, form, and time) and eight quadrants, which facilitates a more systematic exploration of memory in the era of large language models.
(3) From the perspective of enhancing personalized capabilities, we analyze and summarize research related to personal memory.
(4) From the perspective of AI system’s ability to perform complex tasks, we analyze and summarize research related to system memory.
(5) We identify the existing issues and challenges in current memory research and point out potential future directions for development.

 The remainder of the paper is organized as follows:
In Section 2, we present a detailed description of human memory and AI systems’ memory, comparing their differences and relationships, and introduce the classification method for memory based on three dimensions (object, form, and time) and eight quadrants.
In Section 3, we summarize research related to personal memory, aimed at enhancing the personalized response capabilities of AI systems.
In Section 4, we summarize research related to system memory, aimed at improving AI systems’ ability to perform complex tasks.
In Section 5, we analyze some open issues related to memory and point out potential future directions for development.
Finally, in Section 6, we conclude the survey. 

 2 Overview 

 The human brain has evolved complex yet efficient memory mechanisms over a long period, enabling it to encode, store, and recall information effectively  [ 9 ] .
Accordingly, in the development of AI systems, we can draw insights from human memory to design effective & efficient memory mechanisms or systems.
In this section, we will first describe in detail the complex memory mechanisms and related memory systems of the human brain from the perspective of memory neuroscience.
Then, we will discuss the memory mechanisms and types specific to LLM-driven AI systems.
Finally, based on the memory features of LLM-driven AI systems, we will systematically review and categorize existing work from different dimensions. 

 2.1 Human Memory 

 Human memory typically relies on different memory systems to process information for various purposes, such as working memory for temporarily storing and processing information to support ongoing cognitive activities, and episodic memory for recording personal experiences and events for a long time  [ 11 ] . 

 2.1.1 Short-Term and Long-Term Memory 

 Based on the time range, human memory can be roughly divided into short-term memory and long-term memory according to the well-known Multi-Store Model (or Atkinson-Shiffrin Memory Model)  [ 22 ] . 

 Short-Term Memory 

 Short-term memory is a temporary storage system that holds small amounts of information for brief periods, typically ranging from seconds to minutes.
It includes sensory memory , which briefly captures raw sensory information from the environment (like sights or sounds), and working memory , which actively processes and manipulates information to complete tasks such as problem-solving or learning.
Together, these components allow humans to temporarily hold and work with information before either discarding it or transferring it to long-term memory. 

 • 

 Sensory memory : Sensory memory is the brief storage of sensory information we acquire from the external world, including iconic memory (visual), echoic memory (auditory), haptic memory (touch), and other sensory data. It typically lasts only a few milliseconds to a few seconds. Some sensory memories are transferred to working memory, while others are eventually stored in long-term memory (such as episodic memory). 

 • 

 Working memory : Working memory is the system we use to temporarily store and process information. It not only helps us maintain current thoughts but also plays a role in decision-making and problem-solving. For example, when solving a math problem, it allows us to keep track of both the problem and the steps involved in finding the solution. 

 Long-Term Memory 

 Long-term memory is a storage system that holds information for extended periods, ranging from minutes to a lifetime.
It includes explicit memory , which involves conscious recall of facts and events, and implicit memory , which involves unconscious skills and habits, like riding a bike.
These two types work together to help humans retain knowledge, experiences, and learned abilities over time. 

 • 

 Explicit memory : Explicit memory, also known as declarative memory , refers to memories that we can easily verbalize or declare. It can be further divided into episodic memory and semantic memory. Episodic memory refers to memories related to personal experiences and events, such as what you had for lunch. This type of memory is typically broken down into stages like encoding, storage, and retrieval. Semantic memory , on the other hand, refers to memories related to facts and knowledge, such as knowing that the Earth is round or that the Earth orbits the Sun. 

 • 

 Implicit memory : Implicit memory, also known as non-declarative memory , refers to memories that are difficult to describe in words. It is associated with habits, skills, and procedures, and does not require conscious recall. Procedural memory (or "muscle memory") is a typical form of implicit memory. It refers to memories gained through actions, such as riding a bicycle or playing the piano. The planning and coordination of movements are key components of procedural memory. 

 Multiple memory systems typically operate simultaneously, storing information in various ways across different brain regions. These memory systems are not completely independent; they interact with each other and, in many cases, depend on one another.
For example, when you hear a new song, the sensory memory in your ears and the brain regions responsible for processing sound will become active, storing the sound of the song for a few seconds. This sound is then transferred to your working memory system.
As you use your working memory and consciously think about the song, your episodic memory will automatically activate, recalling where you heard the song and what you were doing at the time.
As you hear the song in different places and at different times, a new semantic memory gradually forms, linking the melody of the song with its title. So, when you hear the song again, you’ll remember the song’s title, rather than a specific instance from your multiple listening experiences.
When you practice playing the song on the guitar, your procedural memory will remember the finger movements involved in playing the song. 

 2.1.2 Memory Mechanisms 

 Memory is the ability to encode, store and recall information.
The three main processes involved in human memory are therefore encoding (the process of acquiring and processing information into a form that can be stored), storage (the retention of encoded information over time in short-term or long-term memory), and retrieval ( recall , the process of accessing and bringing stored information back into conscious awareness when needed). 

 • 

 Encoding Memory encoding is the process of changing sensory information into a form that our brain can cope with and store effectively. In particular, there are different types of encoding in terms of how information is processed, such as visual encoding , which involves processing information based on its visual features like color, shape, or texture; acoustic encoding , which focuses on the auditory characteristics of information, such as pitch, tone, or rhythm; and semantic encoding , which is based on the meaning of the information, making it easier to structure and remember. In addition, there are many approaches to make our brain better at encoding memory, such as mnemonics , which involve using acronyms or peg-word systems to aid recall, chunking , where information is broken down into smaller, meaningful units to enhance retention, imagination , which strengthens encoding by linking images to words, and association , where new information is connected to prior knowledge to improve understanding and long-term memory storage. 

 • 

 Storage The storage of memory involves the coordinated activity of multiple brain regions, with key areas including: the prefrontal cortex , which is associated with working memory and decision-making, helping us maintain and process information in the short term; the hippocampus , which helps organize and consolidate information to form new explicit memories (such as episodic memory); the cerebral cortex , which is involved in the storage and retrieval of semantic memory, allowing us to retain facts, concepts, and general knowledge over time; and the cerebellum , which is primarily responsible for procedural memory formed through repetition. 

 • 

 Retrieval Memory retrieval is the ability to access information and get it out of the memory storage. When we recall something, the brain reactivates neural pathways (also called synapses) linked to that memory. The prefrontal cortex helps in bringing memories back to awareness. Similarly, there are different types of memory retrieval, including recognition , where we identify previously encountered information or stimuli, such as recognizing a familiar face or a fact we have learned before; recall , which is the ability to retrieve information from memory without external cues, like remembering a phone number or address from memory; and relearning , a process in which we reacquire previously learned but forgotten information, often at a faster pace than initial learning due to the residual memory traces that still exist. 

 In addition to the fundamental memory processing stages of encoding, storage, and retrieval, human memory also includes consolidation (the process of stabilizing and strengthening memories to facilitate long-term storage), reconsolidation (the modification or updating of previously stored memories when they are reactivated, allowing them to adapt to new information or contexts), reflection (the active review and evaluation of one’s memories to enhance self-awareness, improve learning strategies, and optimize decision-making), and forgetting (the process by which information becomes inaccessible). 

 • 

 Consolidation Memory consolidation refers to the process of converting short-term memory into long-term memory, allowing information to be stably stored in the brain and reducing the likelihood of forgetting. It primarily involves the hippocampus and strengthens neural connections through synaptic plasticity (strengthening of connections between neurons) and systems consolidation (the gradual transfer and reorganization of memories from the hippocampus to the neocortex for long-term storage). 

 • 

 Reconsolidation Memory reconsolidation refers to the process in which a previously stored memory is reactivated, entering an unstable state and requiring reconsolidation to maintain its storage. This process allows for the modification or updating of existing memories to adapt to new information or contexts, potentially leading to memory enhancement, weakening, or distortion. Once a memory is reactivated, it involves the hippocampus and amygdala and may be influenced by emotions, cognitive biases, or new information, resulting in memory adjustment or reshaping. 

 • 

 Reflection Memory reflection refers to the process in which an individual actively reviews, evaluates, and examines their own memory content and processes to enhance self-awareness, adjust learning strategies, or optimize decision-making. It helps improve metacognitive ability, correct memory biases, facilitate deep learning, and regulate emotions. This process primarily relies on the brain’s metacognitive ability (Metacognition) and involves the prefrontal cortex, which monitors and regulates memory functions. 

 • 

 Forgetting Forgetting is a natural process that occurs when the brain fails to retrieve or retain information, which can result from encoding failure (when information is not properly encoded due to lack of attention or meaningful connection), memory decay (when memories fade over time without reinforcement as neural connections weaken), interference (when similar or new memories compete with or overwrite existing ones), retrieval failure (when information is inaccessible due to missing contextual cues despite being stored), or motivated forgetting (when individuals consciously suppress or unconsciously repress traumatic or distressing memories). However, forgetting is a natural and necessary process that enables our brains to filter out irrelevant and outdated information, allowing us to prioritize what is most important for our current needs. 

 2.2 Memory of LLM-driven AI Systems 

 Similar to humans, LLM-driven AI systems also rely on memory systems to encode, store and recall information for future use.
A typical example is the LLM-driven agent system, which leverages memory to enhance the agent system’s abilities in reasoning, planning, personalization, and more  [ 10 ] . 

 2.2.1 Fundamental Dimensions of AI Memory 

 The memory of an LLM-driven AI system is closely related to the features of the LLM, that define how information is processed, stored, and retrieved based on its architecture and capabilities.
We primarily categorize and organize memory based on three dimensions: object (personal and system memory), form (non-parametric and parametric memory), and time (short-term and long-term memory).
These three dimensions comprehensively capture what type of information is retained (object), how information is stored (form), and how long it is preserved (time), aligning with both the functional structure of LLMs and practical requirements for efficient recall and adaptability. 

 Object Dimension 

 The object dimension is closely tied to the interaction between LLM-driven AI systems and humans, as it defines how information is categorized based on its source and purpose. On one hand, the system receives human input and feedback (i.e., personal memory); on the other hand, it generates a series of intermediate output results during task execution (i.e., system memory). Personal memory helps the system improve its understanding of user behavior and enhances its personalization capabilities, while system memory can strengthen the system’s reasoning ability, such as in approaches like CoT (Chain-of-Thought)  [ 23 ] and ReAct  [ 24 ] . 

 Form Dimension 

 The form dimension focuses on how memory is represented and stored in LLM-driven AI systems, shaping how information is encoded and retrieved. Some memory is embedded within the model’s parameters through training, forming parametric memory, while other memory exists externally in structured databases or retrieval mechanisms, constituting non-parametric memory. Non-parametric memory serves as a supplementary knowledge source that can be dynamically accessed by the large language model, enhancing its ability to retrieve relevant information in real-time, as seen in retrieval-augmented generation (RAG)  [ 25 ] . 

 Time Dimension 

 The time dimension defines how long memory is retained and how it influences the LLM’s interactions over different timescales. Short-term memory refers to contextual information temporarily maintained within the current conversation, enabling coherence and continuity in multi-turn dialogues. In contrast, long-term memory consists of information from past interactions that is stored in an external database and retrieved when needed, allowing the model to retain user-specific knowledge and improve personalization over time. This distinction ensures that the system can balance real-time responsiveness with accumulated learning for enhanced adaptability. 

 In addition to the three primary dimensions discussed above, memory can also be classified based on other criteria, such as modality , which distinguishes between unimodal memory (single data type) and multimodal memory (integrating multiple data types, such as text, images, and audio), or dynamics , which differentiates between static memory (fixed and unchanging) and streaming memory (dynamically updated in real-time). However, these alternative classifications are not considered the primary criteria here, as our focus is on the core structural aspects that most directly influence memory organization and retrieval in LLM-driven AI systems. 

 2.2.2 Parallels Between Human and AI Memory 

 Figure 1: Illustrating the parallels between human and AI memory. 

 The memory of LLM-driven AI system exhibits similarities to human memory in terms of structure and function. Human memory is generally categorized into short-term memory and long-term memory, a distinction that also applies to AI memory systems. Below, we draw a direct comparison between these categories, mapping human cognitive memory processes to their counterparts in intelligent AI systems.
Figure  1 illustrates the parallels between human and AI memory. 

 • 

 Sensory Memory : When an LLM-driven AI system perceives external information, it converts inputs such as text, images, speech, and video into machine-processable signals. This initial stage of information processing is analogous to human sensory memory, where raw data is briefly held before further cognitive processing. If these signals undergo additional processing, they transition into working memory, facilitating reasoning and decision-making. However, if no further processing or storage occurs, the information is quickly discarded, mirroring the transient nature of human sensory memory. 

 • 

 Working Memory : The working memory of an AI system serves as a temporary storage and processing mechanism, enabling real-time reasoning and decision-making. It encompasses personal memory, such as contextual information retained during multi-turn dialogues, and system memory, including the chain of thoughts generated during task execution. As a form of short-term memory, working memory can undergo further processing and consolidation, eventually transitioning into long-term memory (e.g., episodic memory) that can be retrieved for future use. Additionally, during inference, large language models generate intermediate computational results, such as KV-Caches, which act as a form of parametric short-term memory that enhances efficiency by accelerating the inference process. 

 • 

 Explicit Memory : The explicit memory of an AI system can be categorized into two distinct components. The first is non-parametric long-term memory, which involves the storage and retrieval of user-specific information, allowing the system to retain and utilize personalized data—analogous to episodic memory in humans. The second is parametric long-term memory, where factual knowledge and learned information are embedded within the model’s parameters, forming an internalized knowledge base—corresponding to semantic memory in human cognition. Together, these components enable the system to recall past interactions and apply acquired knowledge effectively. 

 • 

 Implicit Memory : The implicit memory of an AI system encompasses the learned processes and patterns involved in task execution, enabling the development of specialized skills for specific tasks—analogous to procedural memory in humans.
This form of memory can parallel the human process of learning from both successes and failures in a non-parameterized manner, involving the reflection and refinement of accumulated traces, which allows the retention and replication of effective strategies from past experiences.
Additionally, it can be encoded within the model’s parameters, enabling the system to internalize task-related knowledge and perform operations efficiently without the need for explicit recall. 

 Beyond these parallels, insights from human memory can further guide the design of more effective and efficient AI memory systems, enhancing their ability to process, store, and retrieve information in a more structured and adaptive manner. 

 2.2.3 3D-8Q Memory Taxonomy 

 Building upon the three fundamental memory dimensions—object (personal & system), form (non-parametric & parametric), and time (short-term & long-term)—as well as the established parallels between human and AI memory, we propose a three-dimensional, eight-quadrant (3D-8Q) memory taxonomy for AI memory.
This memory taxonomy systematically categorizes AI memory based on its function, storage mechanism, and retention duration, providing a structured approach to understanding and optimizing AI memory systems.
Table  1 presents the eight quadrants and their respective roles and functions. 

 Object 
 Form 
 Time 
 Quadrant 

 Role 

 Function 

 Personal 
 Non-Parametric 
 Short-Term 
 I 

 Working Memory 

 Supports real-time context supplementation, enhancing the AI’s ability to maintain coherent interactions within a session. 

 Long-Term 
 II 

 Episodic Memory 

 Enables memory retention beyond session limits, allowing the system to recall and retrieve past user interactions for personalization. 

 Parametric 
 Short-Term 
 III 

 Working Memory 

 Temporarily enhances contextual understanding in ongoing interactions, improving response relevance and coherence. 

 Long-Term 
 IV 

 Semantic Memory 

 Facilitates the continuous integration of newly acquired knowledge into the model, improving adaptability and personalization 

 System 
 Non-Parametric 
 Short-Term 
 V 

 Working Memory 

 Assists in complex reasoning and decision-making by storing intermediate outputs such as chain-of-thought prompts. 

 Long-Term 
 VI 

 Procedural Memory 

 Captures historical experiences and self-reflection insights, enabling the AI to refine its reasoning and problem-solving skills over time. 

 Parametric 
 Short-Term 
 VII 

 Working Memory 

 Enhances computational efficiency through temporary parametric storage mechanisms such as KV-Caches, optimizing inference speed and reducing resource consumption. 

 Long-Term 
 VIII 

 Semantic Memory Procedural Memory 

 Forms a foundational knowledge base encoded in the model’s parameters, serving as a long-term repository of factual & conceptual knowledge and task-related knowledge. 

 Table 1: Three-dimensional, eight-quadrant (3D-8Q) memory taxonomy for LLM-driven AI systems. 

 Next, we will provide insights and descriptions of existing works from the perspectives of personal memory (in Section  3 ) and system memory (in Section  4 ). In particualr, personal memory focuses more on the individual data perceived and observed by the model from the environment, while system memory emphasizes the system’s internal or endogenous memory, such as the intermediate memory generated during task execution. 

 3 Personal Memory 

 Personal memory refers to the process of storing and utilizing human input and response data during interactions with an LLM-driven AI system.
The development and application of personal memory play a crucial role in enhancing AI systems’ personalization capabilities and improving user experience.
In this section, we explore the concept of personal memory and relevant research, examining both non-parametric and parametric approaches to its construction and implementation.
Table  2 shows the categories, features, and related research work of personal memory. 

 Quadrant 

 Dimension 

 Feature 

 Models 

 I 

 Personal Non-Parametric Short-Term 

 Multi-Turn Dialogue 

 ChatGPT  [ 26 ] , DeepSeek-Chat  [ 27 ] , Claude  [ 28 ] , QWEN-CHAT  [ 29 ] , Llama 2-Chat  [ 30 ] , Gemini  [ 31 ] , PANGU-BOT  [ 32 ] , ChatGLM  [ 33 ] , OpenAssistant  [ 34 ] 

 II 

 Personal Non-Parametric Long-Term 

 Personal Assistant 

 ChatGPT Memory  [ 18 ] , Apple Intelligence  [ 19 ] , Microsoft Recall  [ 35 ] , Me.bot  [ 36 ] 

 Open-Source Framework 

 MemoryScope  [ 21 ] , mem0  [ 20 ] , Memary  [ 37 ] , LangGraph Memory  [ 38 ] , Charlie Mnemonic  [ 39 ] , Memobase  [ 40 ] , Letta  [ 41 ] , Cognee  [ 42 ] 

 Construction 

 MPC  [ 43 ] , RET-LLM  [ 44 ] , MemoryBank  [ 17 ] , MemGPT  [ 45 ] , KGT  [ 46 ] , Evolving Conditional Memory  [ 47 ] , SECOM  [ 48 ] , Memory 3   [ 49 ] , MemInsight  [ 50 ] 

 Management 

 MemoChat  [ 51 ] , MemoryBank  [ 17 ] , RMM  [ 52 ] , LD-Agent  [ 53 ] , A-MEM  [ 54 ] , Generative Agents  [ 55 ] , EMG-RAG  [ 56 ] , KGT  [ 46 ] , LLM-Rsum  [ 57 ] , COMEDY  [ 58 ] 

 Retrieval 

 RET-LLM  [ 44 ] , ChatDB  [ 59 ] , Human-like Memory  [ 60 ] , HippoRAG  [ 13 ] , HippoRAG 2  [ 61 ] , EgoRAG  [ 62 ] , MemInsight  [ 50 ] 

 Usage 

 MemoCRS  [ 63 ] , RecMind  [ 64 ] , RecAgent  [ 65 ] , InteRecAgent  [ 66 ] , SCM  [ 67 ] , ChatDev  [ 68 ] , MetaAgents  [ 69 ] , S 3   [ 70 ] , TradingGPT  [ 71 ] , Memolet  [ 72 ] , Synaptic Resonance  [ 14 ] , MemReasoner  [ 73 ] 

 Benchmark 

 MADial-Bench  [ 74 ] , LOCOMO  [ 75 ] , MemDaily  [ 76 ] , ChMapData  [ 77 ] , MSC  [ 78 ] , MMRC  [ 79 ] , Ego4D  [ 80 ] , EgoLife  [ 62 ] , BABILong  [ 81 , 82 ] 

 III 

 Personal Parametric Short-Term 

 Caching for Acceleration 

 Prompt Cache  [ 83 ] , Contextual Retrieval  [ 84 ] 

 IV 

 Personal Parametric Long-Term 

 Knowledge Editing 

 Character-LLM  [ 85 ] , AI-Native Memory  [ 36 ] , MemoRAG  [ 86 ] , Echo  [ 87 ] 

 Table 2: Personal Memory 

 3.1 Contextual Personal Memory 

 In personal memory, the non-parametric contextual memory that can be loaded is generally divided into two categories: the short-term memory of the current session’s multi-turn dialogue and the long-term memory of historical dialogues across sessions.
The former can effectively supplement contextual information, while the latter can effectively fill in missing information and overcome the limitations of context length. 

 3.1.1 Loading Multi-Turn Dialogue (Quadrant-I) 

 In multi-turn dialogue scenarios, the conversation history of the current session can significantly enhance the LLM-driven AI system’s understanding of the user’s real-time intent, leading to more relevant and contextually appropriate responses.
Many modern dialogue systems are capable of handling multi-turn conversations and fully consider the current dialogue context in their responses.
Notable examples include ChatGPT  [ 26 ] , DeepSeek-Chat  [ 27 ] , and Claude  [ 28 ] , which excel at maintaining coherence and relevance over extended interactions. 

 For instance, ChatGPT  [ 26 ] is a prime example of a multi-turn dialogue system where the conversation history of the current session serves as short-term memory, helping to supplement the contextual information of the dialogue.
In ChatGPT, the dialogue memory is encoded in a role-content format, with distinct roles such as “User” and “Assistant”.
This encoding allows the system to maintain clarity regarding the speaker and the flow of the conversation. 

 Through effective dialogue management at different levels, including “Assistant”, “Threads”, “Messages”, and “Runs”, the system can precisely track the state of each turn and each step of the conversation, ensuring continuity and consistency in interactions.
Additionally, when the conversation length becomes too extensive, the dialogue system manages the conversation’s input by truncating the number of turns, thereby preventing the input from exceeding the model’s length limitations.
This ensures that the system can continue processing the dialogue without losing track of essential context, maintaining the effectiveness of multi-turn interactions. 

 3.1.2 Memory Retrieval-Augmented Generation (Quadrant-II) 

 In cross-session dialogue scenarios, retrieving relevant user long-term memories from historical conversations can effectively supplement missing information in the current session, such as personal preferences and character relationships.
The advantage of memory retrieval-augmented generation is that large language models (LLMs) do not need to load all multi-session conversations.
Given the limited length of LLMs’ context windows—even when extended to millions of tokens—retrieving relevant information from historical sessions is also more efficient and cost-effective in terms of computation.
In addition to multi-session conversations, long-term personal memory also encompasses users’ behavioral history, preferences, and interaction records with AI agents over an extended period of time. 

 By leveraging retrieval-augmented generation from long-term memory, LLM-driven AI systems can better tailor their responses and behaviors, thereby improving user satisfaction and engagement.
For instance, a personal assistant that remembers a user’s preferred news sources can prioritize those outlets in daily briefings, while a recommendation system that understands past viewing habits can suggest content more aligned with the user’s tastes.
Currently, many commercial and open-source platforms are striving to construct and utilize long-term memory for personalized AI systems—for example, ChatGPT Memory  [ 18 ] and Me.bot  [ 36 ] for personal assistants, and MemoryScope  [ 21 ] and mem0  [ 20 ] as open-source frameworks.
Long-term personal memory typically follows four core processing stages: construction , management , retrieval , and usage .
The second section of Table  2 (organized by rows) provides an overview of existing work on personal non-parametric long-term memory, classified based on their primary contributions. 

 Construction 

 The construction of user memory requires extraction and refinement from raw memory data, such as multi-turn conversations. This process is analogous to human memory consolidation—the process of stabilizing and strengthening memories to facilitate their long-term storage.
Well-organized long-term memory enhances both the efficiency of storage and the effectiveness of retrieval in user memory.
For example, MemoryBank  [ 17 ] leverages a memory module to store conversation histories and summaries of key events, enabling the construction of a long-term user profile.
Similarly, RET-LLM  [ 44 ] uses its memory module to retain essential factual knowledge about the external world, allowing the agent to monitor and update real-time environmental context relevant to the user.
In addition, to accommodate different types of memory, a variety of storage formats have been developed, including key-value , graph , and vector representations.
Specifically, key-value formats  [ 44 , 50 , 63 ] enable efficient access to structured information such as user facts and preferences.
 Graph -based formats  [ 46 , 13 , 61 , 20 ] are designed to capture and represent relationships among entities, such as individuals and events.
Meanwhile, vector formats  [ 17 , 48 , 20 ] , which are typically derived from textual, visual, or audio memory representations, are utilized to encode the semantic meaning and contextual information of conversations. 

 Management 

 The management of user memory involves further processing and refinement of previously constructed memories, such as deduplication, merging, and conflict resolution. This process is analogous to human memory reconsolidation and reflection, where existing memories are reactivated, updated, and integrated to maintain coherence and relevance over time.
For instance, Reflective Memory Management (RMM)  [ 52 ] is a user long-term memory management framework that combines Prospective Reflection for dynamic summarization with Retrospective Reflection for retrieval optimization via reinforcement learning.
This dual-process approach addresses limitations such as rigid memory granularity and fixed retrieval mechanisms, enhancing the accuracy and flexibility of long-term memory management.
LD-Agent  [ 53 ] enhances long-term dialogue personalization and consistency by constructing personalized persona information for both users and agents through a dynamic persona modeling module, while integrating retrieved memories to optimize response generation.
A-MEM  [ 54 ] introduces a self-organizing memory system inspired by the Zettelkasten method  [ 88 ] , which constructs interconnected knowledge networks through dynamic indexing, linking, and memory evolution, enabling LLM agents to more flexibly organize, update, and retrieve long-term memories, thereby enhancing task adaptability and contextual awareness.
In addition, MemoryBank  [ 17 ] incorporates a memory updating mechanism inspired by the Ebbinghaus Forgetting Curve  [ 89 ] , allowing the AI to forget or reinforce memories based on the time elapsed and their relative importance, thereby enabling a more human-like memory system and enhancing the user experience. 

 Retrieval 

 Retrieving personal memory involves identifying memory entries relevant to the user’s current request, and the retrieval method is closely tied to how the memory is stored.
For key-value memory, ChatDB  [ 59 ] performs retrieval using SQL queries over structured databases.
RET-LLM  [ 44 ] , on the other hand, employs a fuzzy search to retrieve triplet-structured memories, where information is stored as relationships between two entities connected by a predefined relation.
For graph-based memory, HippoRAG  [ 13 ] constructs knowledge graphs over entities, phrases, and summarization to recall more relative and comprehensive memories, while HippoRAG 2  [ 61 ] further combines original passages with phrase-based knowledge graphs to incorporate both conceptual and contextual information.
For vector memory, MemoryBank  [ 17 ] adopts a dual-tower dense retrieval model, similar to Dense Passage Retrieval  [ 90 ] , to accurately identify relevant memories. The resulting vector representations are then indexed using FAISS  [ 91 ] for efficient similarity-based retrieval. 

 Usage 

 The use of personal memory can effectively empower downstream applications with personalization, enhancing the user’s individualized experience.
For instance, the recalled relevant memory is used as contextual information to enhance the personalized recommendation and response capability of the conversational recommender agents  [ 63 , 64 , 65 , 66 ] , improving the personalized user experience.
In addition to memory-augmented personalized dialogue and recommendation, personal memory can also be leveraged to enhance a wide range of applications, including software development  [ 68 ] , social-network simulation  [ 69 , 70 ] , and financial trading  [ 71 ] . 

 To facilitate in-depth research on personal memory, a variety of memory-related benchmarks have emerged in recent years, including long-term conversational memory (MADial-Bench  [ 74 ] , LOCOMO  [ 75 ] , MSC  [ 78 ] ), everyday life memory (MemDaily  [ 76 ] ), memory-aware proactive dialogue (ChMapData  [ 77 ] ), multimodal dialogue memory (MMRC  [ 79 ] ), egocentric video understanding (Ego4D  [ 80 ] , EgoLife  [ 62 ] ), and long-context reasoning-in-a-haystack (BABILong  [ 81 , 82 ] ). 

 3.2 Parametric Personal Memory 

 In addition to external non-parametric memory, a user’s personal memory can also be stored parametrically. Specifically, personal data can be used to fine-tune an LLM, embedding the memory directly into its parameters (i.e., parametric long-term memory) to create a personalized LLM . Alternatively, historical dialogues can be cached as prompts during inference (i.e., parametric short-term memory), enabling quick reuse in future interactions. 

 3.2.1 Memory Caching For Acceleration (Quadrant-III) 

 Personal parametric short-term memory typically refers to intermediate attention states produced by the LLM when processing personal data, which is usually utilized as memory caches to accelerate inference.
Specifically, prompt caching  [ 83 ] is usually used as an efficient data management technique that allows for the pre-storage of large amounts of personal data or information that may be frequently requested, such as a user’s conversational history.
For instance, during multi-turn dialogues, the dialogue system can quickly provide the personal context information directly from the parametric memory cache, avoiding the need to recalculate or retrieve it from the original data source, saving both time and resources.
Major platforms such as DeepSeek, Anthropic, OpenAI, and Google employ prompt caching to reduce API call costs and improve response speed in dialogue scenarios.
Moreover, personal parametric short-term memory can enhance the performance of retrieval-augmented generation (RAG) through Contextual Retrieval  [ 84 ] , where prompt caching helps reduce the overhead of generating contextualized chunks.
At present, research specifically targeting caching techniques for personal memory data remains limited. Instead, most existing work considers caching as a fundamental capability of system memory, particularly in the context of key-value (KV) management and KV reuse. A more detailed discussion of these aspects is provided in Section  4 . 

 3.2.2 Personalized Knowledge Editing (Quadrant-IV) 

 Personal parametric long-term memory utilizes personalized Knowledge Editing technology  [ 92 ] , such as Parameter-Efficient Fine-Tuning (PEFT)  [ 93 ] , to encode personal data into the LLM’s parameters in a parametric manner, thereby facilitating the long-term, parameterized storage of memory.
For instance, Character-LLM  [ 85 ] enables the role-playing of specific characters, such as Beethoven, Queen Cleopatra, Julius Caesar, etc., by training large language models to remember the roles and experiences of these characters.
AI-Native Memory  [ 36 ] proposes using deep neural network models, specifically large language models (LLMs), as Lifelong Personal Models (LPMs) to parameterize, compress, and continuously evolve personal memory through user interactions, enabling a more comprehensive understanding of the user.
MemoRAG  [ 86 ] utilizes LLM parametric memory to store user conversation history and preferences, forming a personalized global memory that enhances personalization and enables tailored recommendations.
Echo  [ 87 ] is a large language model enhanced with temporal episodic memory, designed to improve performance in applications requiring multi-turn, complex memory-based dialogues.
The parameterization of personal long-term memory presents several challenges, notably the need to fine-tune models on individual user data, which demands substantial computational resources. This requirement significantly hinders the scalability and practical deployment of parametric approaches to long-term personal memory. 

 3.3 Discussion 

 In this section, we describe personal memory and related work from the perspectives of non-parametric and parametric approaches.
Specifically, personal non-parametric short-term memory necessitates efficient mechanisms for memory encoding and management. Existing literature predominantly emphasizes the design and implementation of systems that facilitate the construction, management, retrieval, and effective utilization of a user’s personal non-parametric long-term memory.
In contrast, personal parametric short-term memory can employ techniques such as prompt caching to reduce computational costs and enhance efficiency.
Parametric long-term memory offers advantages in memory compression, thereby supporting a more comprehensive and global representation of the user’s accumulated experiences.
Recent trends in the field indicate a growing interest in integrating both short-term and long-term memory paradigms, wherein parametric and non-parametric memory components complement and reinforce one another.
The subsequent section will present a detailed discussion of system memory and its associated research developments. 

 4 System Memory 

 System memory constitutes a critical component of LLM-driven AI systems.
It encompasses a sequence of intermediate representations or results generated throughout the task execution process.
By leveraging system memory, LLM-driven AI systems can enhance their capabilities in reasoning, planning, and other higher-order cognitive functions.
Moreover, the effective use of system memory contributes to the system’s capacity for self-evolution and continual improvement.
In this section, we examine system memory and its associated research from both non-parametric and parametric perspectives. 

 Quadrant 

 Dimension 

 Feature 

 Models 

 V 

 System Non-Parametric Short-Term 

 Reasoning & Planning Enhancement 

 ReAct  [ 24 ] , RAP  [ 94 ] , Reflexion  [ 95 ] , Talker-Reasoner  [ 96 ] , TPTU  [ 97 ] 

 VI 

 System Non-Parametric Long-Term 

 Reflection & Refinement 

 Buffer of Thoughts  [ 98 ] , AWM  [ 99 ] , Think-in-Memory  [ 100 ] , GITM  [ 101 ] , Voyager  [ 102 ] , Retroformer  [ 103 ] , Expel  [ 104 ] , Synapse  [ 105 ] , MetaGPT  [ 106 ] , Learned Memory Bank  [ 107 ] , M+  [ 108 ] 

 VII 

 System Parametric Short-Term 

 KV Management 

 LookupFFN  [ 109 ] , ChunkKV  [ 110 ] , vLLM  [ 111 ] , FastServe  [ 112 ] , StreamingLLM  [ 113 ] , Orca  [ 114 ] , DistServe  [ 115 ] , LLM.int8()  [ 116 ] , FastGen  [ 117 ] , Train Large, Then Compress  [ 118 ] , Scissorhands  [ 119 ] , H 2 O  [ 120 ] , Mooncake  [ 121 ] , MemServe  [ 122 ] , SLM Se
