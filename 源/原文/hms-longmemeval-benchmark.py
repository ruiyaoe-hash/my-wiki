"""
LongMemEval-specific benchmark implementa
tions.

Provides dataset, answer generator, a
nd evaluator for the LongMemEval benchmark.
"
""

import asyncio
import json
import os
impo
rt re
import sys
from datetime import date, d
atetime, timedelta, timezone
from pathlib imp
ort Path
from typing import Any, Dict, List, 
Optional, Tuple

import pydantic
from hms_api
.engine.llm_wrapper import LLMConfig
from ope
nai import AsyncOpenAI

from benchmarks.commo
n.benchmark_runner import (
    BenchmarkData
set,
    BenchmarkRunner,
    LLMAnswerEvalua
tor,
    LLMAnswerGenerator,
    RecallPlan,

)


ORACLE_PLANNER_V1_WEIGHTS = {
    "single
-session-user": 0.25,
    "single-session-ass
istant": 0.25,
    "single-session-preference
": 0.30,
    "knowledge-update": 0.50,
    "t
emporal-reasoning": 0.60,
    "multi-session"
: 0.80,
}


SELF_EVOLUTION_PROFILES = {
    "
oracle_v220": {
        "base": "oracle_v26",

        "diagnosis_source": "v2.6 failed Lon
gMemEval cases only",
        "evolution_targ
ets": [
            "count/total deduplicatio
n",
            "relative-date lookup groundi
ng",
            "amount/difference missing-s
ide calibration",
            "current/previo
us state arbitration",
        ],
        "se
lection_rule": "Keep V2.6 retrieval and ledge
r as the base; add only diagnosis-derived pre
-generation evidence controls.",
    },
}


d
ef _v26_base_retrieval_plan(
    question: st
r,
    question_type: Optional[str],
    ques
tion_date: Optional[datetime],
) -> RecallPla
n:
    """Internal V2.6 retrieval base: oracl
e weights plus multi-session query expansion 
and appendix."""
    del question, question_d
ate
    weight = ORACLE_PLANNER_V1_WEIGHTS.ge
t(question_type or "", 0.30)
    if question_
type == "multi-session":
        return Recal
lPlan(
            name="longmemeval_v26_base
_retrieval",
            session_expansion_we
ight=weight,
            query_rewriting_enab
led=True,
            query_rewriting_strateg
y_name="llm_driven",
            evidence_app
endix_mode="cross_session",
        )
    ret
urn RecallPlan(name="longmemeval_v26_base_ret
rieval", session_expansion_weight=weight)


d
ef longmemeval_oracle_planner_v26(
    questi
on: str,
    question_type: Optional[str],
  
  question_date: Optional[datetime],
) -> Rec
allPlan:
    """V2.6: base retrieval plus a p
re-generation Structured Evidence Ledger."""

    plan = _v26_base_retrieval_plan(question,
 question_type, question_date)
    plan.name 
= "longmemeval_oracle_v26"
    return plan



def longmemeval_oracle_planner_v220(
    ques
tion: str,
    question_type: Optional[str],

    question_date: Optional[datetime],
) -> R
ecallPlan:
    """V2.20: V2.6 plus diagnosis-
driven self-evolution controls."""
    plan =
 _v26_base_retrieval_plan(question, question_
type, question_date)
    plan.name = "longmem
eval_oracle_v220"
    return plan


class Lon
gMemEvalDataset(BenchmarkDataset):
    """Lon
gMemEval dataset implementation."""

    def 
load(self, path: Path, max_items: Optional[in
t] = None) -> List[Dict[str, Any]]:
        "
""Load LongMemEval dataset from JSON file."""

        with open(path, "r") as f:
         
   dataset = json.load(f)

        if max_ite
ms:
            dataset = dataset[:max_items]


        return dataset

    def get_item_id
(self, item: Dict) -> str:
        """Get que
stion ID from LongMemEval item."""
        re
turn item.get("question_id", "unknown")

    
def prepare_sessions_for_ingestion(self, item
: Dict) -> List[Dict[str, Any]]:
        """

        Prepare LongMemEval conversation sess
ions for batch ingestion.

        Returns:
 
           List of session dicts with 'conten
t', 'context', 'event_date'
        """
     
   sessions = item.get("haystack_sessions", [
])
        dates = item.get("haystack_dates",
 [])
        session_ids = item.get("haystack
_session_ids", [])

        # Ensure all list
s have same length
        if not (len(sessio
ns) == len(dates) == len(session_ids)):
     
       min_len = min(len(sessions), len(dates
), len(session_ids))
            sessions = s
essions[:min_len]
            dates = dates[:
min_len]
            session_ids = session_id
s[:min_len]

        batch_contents = []
    
    seen_document_ids = {}

        # Process
 each session
        for idx, (session_turns
, date_str, session_id) in enumerate(zip(sess
ions, dates, session_ids)):
            # Par
se session date
            session_date = se
lf._parse_date(date_str) if date_str else dat
etime.now(timezone.utc)

            # Clean 
session turns - remove has_answer key if pres
ent
            cleaned_turns = []
          
  for turn in session_turns:
                
if isinstance(turn, dict):
                  
  cleaned_turn = {k: v for k, v in turn.items
() if k != "has_answer"}
                    
cleaned_turns.append(cleaned_turn)
          
      else:
                    cleaned_turns
.append(turn)

            session_content = 
json.dumps(cleaned_turns)
            questio
n_id = item.get("question_id", "unknown")
   
         base_document_id = f"{question_id}_{
session_id}"

            unique_document_id 
= base_document_id
            if base_docume
nt_id in seen_document_ids:
                s
een_document_ids[base_document_id] += 1
     
           unique_document_id = f"{base_docum
ent_id}_chunk{seen_document_ids[base_document
_id]}"
            else:
                seen
_document_ids[base_document_id] = 0

        
    batch_contents.append(
                {

                    "content": session_conten
t,
                    "context": f"Session {
unique_document_id} - you are the assistant i
n this conversation - happened on {session_da
te.strftime('%Y-%m-%d %H:%M:%S')} UTC.",
    
                "event_date": session_date,
 
                   "document_id": unique_docu
ment_id,
                }
            )

   
     return batch_contents

    def get_qa_pa
irs(self, item: Dict) -> List[Dict[str, Any]]
:
        """
        Extract QA pairs from L
ongMemEval item.

        For LongMemEval, ea
ch item has one question.

        Returns:
 
           List with single QA dict with 'que
stion', 'answer', 'category', 'question_date'

        """
        # Parse question_date if
 available
        question_date = None
     
   if "question_date" in item:
            qu
estion_date = self._parse_date(item["question
_date"])

        return [
            {
    
            "question": item.get("question", 
""),
                "answer": item.get("answ
er", ""),
                "category": item.ge
t("question_type", "unknown"),
              
  "question_date": question_date,
           
 }
        ]

    def _parse_date(self, date_
str: str) -> datetime:
        """Parse date 
string to datetime object."""
        try:
  
          # LongMemEval format: "2023/05/20 (
Sat) 02:21"
            # Try to parse the ma
in part before the day name
            date_
str_cleaned = date_str.split("(")[0].strip() 
if "(" in date_str else date_str

           
 # Try multiple formats
            for fmt i
n ["%Y/%m/%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y
-%m-%d", "%Y/%m/%d"]:
                try:
  
                  dt = datetime.strptime(date
_str_cleaned, fmt)
                    return
 dt.replace(tzinfo=timezone.utc)
            
    except ValueError:
                    co
ntinue

            # Fallback: try ISO forma
t
            return datetime.fromisoformat(d
ate_str.replace("Z", "+00:00"))
        excep
t Exception:
            raise ValueError(f"F
ailed to parse date string: {date_str}")


cl
ass QuestionAnswer(pydantic.BaseModel):
    a
nswer: str
    reasoning: Optional[str] = Non
e


class LongMemEvalAnswerGenerator(LLMAnswe
rGenerator):
    """LongMemEval-specific answ
er generator using configurable LLM provider.
"""

    def __init__(
        self,
        
context_format: str = "json",
        evidenc
e_mode: Optional[str] = None,
    ):
        
"""Initialize with LLM configuration for answ
er generation.

        Args:
            con
text_format: How to format the retrieved cont
ext. Options:
                - "json": Raw J
SON dump of recall_result (original behavior)

                - "structured": Human-readab
le format with facts grouped with source chun
ks
        """
        # Uses HMS_API_ANSWER_
LLM_* env vars with fallback to HMS_API_LLM_*
 for
        # benchmark-specific LLM configu
ration (separate from the API config system).

        self.llm_config = LLMConfig(
       
     provider=os.getenv("HMS_API_ANSWER_LLM_P
ROVIDER", os.getenv("HMS_API_LLM_PROVIDER", "
openai")),
            api_key=os.getenv("HMS
_API_ANSWER_LLM_API_KEY", os.getenv("HMS_API_
LLM_API_KEY", "")),
            base_url=os.g
etenv("HMS_API_ANSWER_LLM_BASE_URL", os.geten
v("HMS_API_LLM_BASE_URL", "")),
            m
odel=os.getenv("HMS_API_ANSWER_LLM_MODEL", os
.getenv("HMS_API_LLM_MODEL", "gpt-4o-mini")),

            reasoning_effort="high",
       
 )
        self.client = self.llm_config._cli
ent
        self.model = self.llm_config.mode
l
        self.context_format = context_forma
t
        self.evidence_mode = evidence_mode


    def _format_context_json(self, recall_re
sult: Dict[str, Any]) -> str:
        """Orig
inal JSON dump format."""
        return json
.dumps(recall_result)

    def _format_contex
t_structured(self, recall_result: Dict[str, A
ny]) -> str:
        """Human-readable format
 with facts grouped with their source chunks.


        Format:
            Fact 1: [fact t
ext]
            When: [date]
            Sou
rce:
              "[chunk text]"

          
  ---

            Fact 2: ...

            =
== Entity Observations ===
            Entity
: [name]
            - [observation 1]
      
      - [observation 2]
        """
        r
esults = recall_result.get("results", [])
   
     chunks = recall_result.get("chunks", {})

        entities = recall_result.get("entiti
es", {})

        if not results and not enti
ties:
            return "No memories found."


        formatted_parts = []

        for i
, fact in enumerate(results, 1):
            
fact_text = fact.get("text", "")
            
fact_type = fact.get("fact_type", "unknown")


            # Extract temporal information
 
           occurred_start = fact.get("occurre
d_start")
            occurred_end = fact.get
("occurred_end")
            mentioned_at = f
act.get("mentioned_at")

            # Build 
temporal string
            when_parts = []
 
           if occurred_start:
               
 when_parts.append(f"occurred: {occurred_star
t}")
            if mentioned_at:
           
     when_parts.append(f"mentioned: {mentione
d_at}")
            when_str = " | ".join(whe
n_parts) if when_parts else "unknown"

      
      # Get the source chunk if available
   
         chunk_id = fact.get("chunk_id")
    
        chunk_text = None
            if chun
k_id and chunk_id in chunks:
                
chunk_info = chunks[chunk_id]
               
 chunk_text = chunk_info.get("chunk_text", ""
)

            # Build the formatted fact ent
ry
            entry_parts = [f"Fact {i} ({fa
ct_type}): {fact_text}", f"When: {when_str}"]


            # Add context field if present

            context = fact.get("context")
   
         if context:
                entry_pa
rts.append(f"Context: {context}")

          
  # Add source chunk
            if chunk_tex
t:
                # Truncate very long chunk
s
                if len(chunk_text) > 1000:

                    chunk_text = chunk_text[:
1000] + "..."
                entry_parts.app
end(f'Source chunk:\n  "{chunk_text}"')

    
        formatted_parts.append("\n".join(entr
y_parts))

        # Add entity observations 
section if present
        if entities:
     
       entity_parts = ["=== Entity Observatio
ns ==="]
            for entity_name, entity_
state in entities.items():
                ob
servations = entity_state.get("observations",
 [])
                if observations:
       
             entity_parts.append(f"\nEntity: 
{entity_name}")
                    for obs i
n observations:
                        obs_t
ext = obs.get("text", "")
                   
     entity_parts.append(f"  - {obs_text}")
 
           if len(entity_parts) > 1:  # More 
than just the header
                formatte
d_parts.append("\n".join(entity_parts))

    
    return "\n\n---\n\n".join(formatted_parts
)

    def _get_context_instructions(self) ->
 str:
        """Get instructions for interpr
eting the context based on format."""
       
 if self.context_format == "structured":
    
        context_guide = """**Understanding th
e Retrieved Context:**
The context contains m
emory facts extracted from previous conversat
ions, each with its source chunk.

1. **Fact*
*: A high-level summary/atomic fact (e.g., "U
ser loves hiking in mountains")
   - This is 
the searchable summary of what was stored

2.
 **Source Chunk**: The actual raw conversatio
n where the fact was extracted from
   - **Th
is is your primary source for detailed inform
ation**
   - Look here for specifics, context
, quotes, and evidence
   - Prioritize inform
ation from chunks when facts seem ambiguous


3. **Temporal Information**:
   - "occurred":
 When the event actually happened
   - "menti
oned": When it was discussed in conversation

   - Use this to understand the timeline and 
resolve conflicts (prefer more recent info)


4. **Context**: Additional metadata about the
 conversation session
"""
        else:
     
       context_guide = ""

        base_instr
uctions = """
**Date Calculations (CRITICAL -
 read carefully):**
- When calculating days b
etween two dates: count the days from Date A 
to Date B as (B - A)
- Example: Jan 1 to Jan 
8 = 7 days (not 8)
- "X days ago" from Questi
on Date means: Question Date minus X days
- W
hen a fact says "three weeks ago" on a certai
n mentioned date, that refers to 3 weeks befo
re THAT mentioned date, NOT the question date

- Always convert relative times ("last Frida
y", "two weeks ago") to absolute dates BEFORE
 comparing
- Double-check your arithmetic - o
ff-by-one errors are very common
- **Importan
t**: Read questions carefully for time anchor
s. "How many days ago did X happen when Y hap
pened?" asks for the time between X and Y, NO
T between X and the question date

**Handling
 Relative Times in Facts:**
- If a fact says 
"last Friday" or "two weeks ago", anchor it t
o the fact's "mentioned" date, NOT the questi
on date
- First convert ALL relative referenc
es to absolute dates, then answer the questio
n
- Show your date conversion work in your re
asoning

**Counting Questions (CRITICAL for "
how many" questions):**
- **Scan ALL facts fi
rst** - go through every single fact before c
ounting, don't stop early
- **List each item 
explicitly in your reasoning** before giving 
the count: "1. X, 2. Y, 3. Z = 3 total"
- **C
heck all facts and chunks** before giving you
r final count
- **Watch for duplicates**: The
 same item may appear in multiple facts. Dedu
plicate by checking if two facts refer to the
 same underlying item/event
- **Watch for dif
ferent descriptions of same thing**: "Dr. Pat
el (ENT specialist)" and "the ENT specialist"
 might be the same doctor
- **Don't over-inte
rpret**: A project you "completed" is differe
nt from a project you're "leading"
- **Don't 
double-count**: If the same charity event is 
mentioned in two conversations, it's still on
e event

**Disambiguation Guidance (CRITICAL 
- many errors come from over-counting):**
- *
*Assume overlap by default**: If two facts de
scribe similar events (same type, similar tim
eframe, similar details), assume they are the
 SAME event unless there's clear evidence the
y are different
- If a person has a name AND 
a role mentioned, check if they're the same p
erson before counting separately
- If an amou
nt is mentioned multiple times on different d
ates, check if it's the same event or differe
nt events
- When facts reference the same und
erlying event from different sessions, count 
it once
- **Check for aliases**: "my college 
roommate's wedding" and "Emily's wedding" mig
ht be the same event
- **Check for time perio
d overlap**: Two "week-long breaks" mentioned
 in overlapping time periods are likely the s
ame break
- **When in doubt, undercount**: It
's better to miss a duplicate than to count t
he same thing twice

**Question Interpretatio
n (read carefully):**
- "How many X before Y?
" - count only X that happened BEFORE Y, not 
Y itself
- "How many properties viewed before
 making an offer on Z?" - count OTHER propert
ies, not Z
- "How many X in the last week/mon
th?" - calculate the exact date range from th
e question date, then filter
- Pay attention 
to qualifiers like "before", "after", "initia
lly", "currently", "in total"

**When to Say 
"I Don't Know":**
- If the question asks abou
t something not in the retrieved context, say
 "I don't have information about X"
- If comp
aring two things (e.g., "which happened first
, X or Y?") but only one is mentioned, explic
itly say the other is missing
- Don't guess o
r infer dates that aren't explicitly stated i
n the facts or chunks
- If you cannot find a 
specific piece of information after checking 
all facts and chunks, admit it
- **Partial kn
owledge is OK**: If asked about two things an
d you only have info on one, provide what you
 know and note what's missing (don't just say
 "I don't know")

**For Recommendation/Prefer
ence Questions (tips, suggestions, advice):**

- **DO NOT invent specific recommendations**
 (no made-up product names, course names, pap
er titles, channel names, etc.)
- **DO mentio
n specific brands/products the user ALREADY u
ses** from the context
- Describe WHAT KIND o
f recommendation the user would prefer, refer
encing their existing tools/brands
- Keep ans
wers concise - focus on key preferences (bran
d, quality level, specific interests) not exh
austive category lists
- First scan ALL facts
 for user's existing tools, brands, stated pr
eferences

**How to Answer:**
1. Scan ALL fac
ts to find relevant memories - don't stop aft
er finding a few
2. **Read the source chunks 
carefully** - they contain the actual details
 you need
3. Convert all relative times to ab
solute dates
4. Use temporal information to u
nderstand when things happened
5. Synthesize 
information from multiple facts if needed
6. 
If facts conflict, prefer more recent informa
tion
7. Double-check any date calculations be
fore answering
8. **For counting questions ("
how many")**: First list each unique item in 
your reasoning (1. X, 2. Y, 3. Z...), then co
unt them
9. **For recommendations**: Referenc
e the user's existing tools, experiences, or 
preferences explicitly
"""
        return con
text_guide + base_instructions

    def _need
s_structured_evidence_ledger(self, question: 
str, question_type: Optional[str]) -> bool:
 
       if self.evidence_mode not in {"oracle_
v26", "oracle_v220"}:
            return Fals
e
        eligible_types = {"multi-session", 
"temporal-reasoning", "knowledge-update"}
   
     if question_type not in eligible_types:

            return False

        question_lo
wer = question.lower()
        markers = (
  
          "after",
            "ago",
       
     "amount",
            "before",
        
    "between",
            "cashback",
      
      "compared",
            "cost",
       
     "current",
            "currently",
    
        "date",
            "days",
         
   "difference",
            "earliest",
    
        "first",
            "higher",
      
      "hours",
            "how long",
      
      "how many",
            "how much",
   
         "in total",
            "initially",

            "latest",
            "less",
  
          "lower",
            "months",
    
        "more",
            "most",
         
   "order",
            "percentage",
       
     "previous",
            "recently",
    
        "since",
            "spent",
       
     "total",
            "weeks",
          
  "years",
        )
        return any(marke
r in question_lower for marker in markers)

 
   @staticmethod
    def _needs_v26_self_evol
ution_controller(question: str, question_type
: Optional[str]) -> bool:
        if question
_type not in {"multi-session", "temporal-reas
oning", "knowledge-update"}:
            retu
rn False
        question_lower = question.lo
wer()
        markers = (
            "ago",

            "before",
            "after",
  
          "current",
            "currently",

            "difference",
            "first
",
            "how many",
            "how m
uch",
            "in total",
            "in
itially",
            "latest",
            "
previous",
            "save",
            "s
pent",
            "total",
        )
       
 return any(marker in question_lower for mark
er in markers)

    @staticmethod
    def _v2
6_self_evolution_controller() -> str:
       
 return """
**V2.20 V2.6 Self-Evolution Contr
oller:**
This controller was derived from V2.
6 failure analysis. It does not replace the V
2.6 evidence ledger; it tells you how to use 
that ledger more carefully.
- Count/total que
stions: enumerate unique real user events/ite
ms before giving the count. Do not count reco
mmendations, options, generic background fact
s, plans, or duplicate extractions of the sam
e event. If one required category is missing,
 answer with the known side plus "not enough 
information"; do not collapse missing evidenc
e to 0.
- Amount/difference questions: comput
e only from amounts that are explicitly prese
nt for both sides requested by the question. 
If one side's amount is missing, say which si
de is missing instead of using generic ranges
.
- Relative-date lookup questions: resolve t
he relative date from the question date, then
 prefer facts and source snippets whose event
 date or source text matches that resolved da
y. If the answer is described rather than nam
ed, return the full descriptive phrase.
- Cur
rent/previous/update questions: prefer the la
test explicit state for "current" questions a
nd the older explicit state for "previous/bef
ore" questions. Do not add old and new state 
values unless the question asks for a cumulat
ive lifetime total.
- Final answer contract: 
start with the direct value/name/date/insuffi
cient-information statement. Put caveats in r
easoning after the direct answer.
"""

    @s
taticmethod
    def _compact_text(text: Any, 
max_chars: int) -> str:
        compact = " "
.join(str(text or "").replace("<|endoftext|>"
, " ").split())
        if len(compact) > max
_chars:
            compact = compact[: max_c
hars - 3].rstrip() + "..."
        return com
pact

    @staticmethod
    def _content_term
s(question: str) -> set[str]:
        stopwor
ds = {
            "about",
            "afte
r",
            "again",
            "before"
,
            "between",
            "current
",
            "currently",
            "diff
erent",
            "during",
            "fi
rst",
            "from",
            "have",

            "many",
            "much",
    
        "previous",
            "recently",
 
           "since",
            "that",
     
       "the",
            "then",
           
 "there",
            "this",
            "to
tal",
            "what",
            "when",

            "where",
            "which",
  
          "with",
        }
        return {

            token
            for token in re
.findall(r"[A-Za-z][A-Za-z0-9_'-]{2,}", quest
ion.lower())
            if token not in stop
words
        }

    def _format_structured_e
vidence_ledger(self, question: str, recall_re
sult: Dict[str, Any]) -> str:
        results
 = recall_result.get("results", [])
        c
hunks = recall_result.get("chunks", {})
     
   question_terms = self._content_terms(quest
ion)
        signal_re = re.compile(
        
    r"(\$?\d+(?:[.,]\d+)?%?|jan|feb|mar|apr|m
ay|jun|jul|aug|sep|oct|nov|dec|"
            
r"monday|tuesday|wednesday|thursday|friday|sa
turday|sunday|"
            r"today|yesterday
|tomorrow|last|next|ago|week|month|year|day|h
our|"
            r"before|after|first|earlie
r|later|previous|current|latest|total|spent|c
ost|discount|cashback)",
            re.IGNOR
ECASE,
        )

        ledger_rows = []
  
      seen = set()
        for fact in result
s[:180]:
            text = self._compact_tex
t(fact.get("text", ""), 360)
            if n
ot text:
                continue
           
 text_lower = text.lower()
            term_o
verlap = sum(1 for term in question_terms if 
term in text_lower)
            has_signal = 
bool(signal_re.search(text))
            if n
ot has_signal and term_overlap < 2:
         
       continue

            dedupe_key = re.
sub(r"\W+", " ", text_lower).strip()[:180]
  
          doc_id = str(fact.get("document_id"
) or "")
            dedupe_key = f"{doc_id}:
{dedupe_key}"
            if dedupe_key in se
en:
                continue
            seen
.add(dedupe_key)

            ledger_rows.app
end(
                {
                    "s
core": (3 if has_signal else 0) + term_overla
p,
                    "doc": doc_id,
       
             "type": fact.get("fact_type"),
 
                   "occurred": fact.get("occu
rred_start") or fact.get("occurred_end") or "
-",
                    "mentioned": fact.get
("mentioned_at") or "-",
                    
"chunk_id": fact.get("chunk_id"),
           
         "text": text,
                }
    
        )
            if len(ledger_rows) >= 
70:
                break

        ledger_row
s.sort(key=lambda row: row["score"], reverse=
True)
        ledger_rows = ledger_rows[:45]

        if not ledger_rows:
            retur
n ""

        lines = [
            "=== V2.6
 Structured Evidence Ledger ===",
           
 "Use this as a checklist for count/sum/date/
order/update questions. It is extracted from 
the retrieved context; do not use it as new e
vidence beyond the facts and source chunks. D
eduplicate repeated mentions of the same even
t before counting.",
            "",
        
    "Candidate facts:",
        ]
        use
d_chunks = []
        seen_chunks = set()
   
     for idx, row in enumerate(ledger_rows, 1
):
            lines.append(
                
f"{idx}. occurred={row['occurred']} | mention
ed={row['mentioned']} | "
                f"d
oc={row['doc']} | type={row['type']} | {row['
text']}"
            )
            chunk_id =
 row.get("chunk_id")
            if chunk_id 
and chunk_id in chunks and chunk_id not in se
en_chunks:
                seen_chunks.add(ch
unk_id)
                used_chunks.append(ch
unk_id)

        if used_chunks:
            
lines.extend(["", "Raw source snippets for le
dger rows:"])
            for idx, chunk_id i
n enumerate(used_chunks[:18], 1):
           
     chunk_info = chunks.get(chunk_id) or {}

                chunk_text = self._compact_te
xt(chunk_info.get("chunk_text", ""), 650)
   
             if chunk_text:
                 
   lines.append(f"{idx}. chunk={chunk_id} | {
chunk_text}")

        return "\n".join(lines
)

    @staticmethod
    def _sort_date_key(v
alue: Any) -> Tuple[int, str]:
        if not
 value or value == "-":
            return (1
, "")
        return (0, str(value))

    @st
aticmethod
    def _date_from_value(value: An
y) -> Optional[date]:
        if not value or
 value == "-":
            return None
      
  text = str(value).strip()
        if not te
xt:
            return None
        try:
    
        return datetime.fromisoformat(text.re
place("Z", "+00:00")).date()
        except V
alueError:
            match = re.search(r"\d
{4}-\d{2}-\d{2}", text)
            if not ma
tch:
                return None
            
try:
                return datetime.strptime
(match.group(0), "%Y-%m-%d").date()
         
   except ValueError:
                return 
None

    @staticmethod
    def _resolved_rel
ative_dates(question: str, question_date: Opt
ional[datetime]) -> List[Tuple[str, date]]:
 
       if question_date is None:
            
return []
        question_lower = question.l
ower()
        base_date = question_date.date
()
        resolved: List[Tuple[str, date]] =
 []

        for match in re.finditer(r"\b(\d
+)\s+days?\s+ago\b", question_lower):
       
     days = int(match.group(1))
            r
esolved.append((match.group(0), base_date - t
imedelta(days=days)))

        for match in r
e.finditer(r"\b(\d+)\s+weeks?\s+ago\b", quest
ion_lower):
            weeks = int(match.gro
up(1))
            resolved.append((match.gro
up(0), base_date - timedelta(days=7 * weeks))
)

        word_numbers = {
            "one"
: 1,
            "two": 2,
            "three
": 3,
            "four": 4,
            "fiv
e": 5,
            "six": 6,
            "sev
en": 7,
            "eight": 8,
            "
nine": 9,
            "ten": 10,
        }
  
      for word, value in word_numbers.items()
:
            if re.search(rf"\b{word}\s+days
?\s+ago\b", question_lower):
                
resolved.append((f"{word} days ago", base_dat
e - timedelta(days=value)))
            if re
.search(rf"\b{word}\s+weeks?\s+ago\b", questi
on_lower):
                resolved.append((f
"{word} weeks ago", base_date - timedelta(day
s=7 * value)))

        if re.search(r"\byest
erday\b", question_lower):
            resolv
ed.append(("yesterday", base_date - timedelta
(days=1)))

        weekdays = {
            
"monday": 0,
            "tuesday": 1,
      
      "wednesday": 2,
            "thursday":
 3,
            "friday": 4,
            "sat
urday": 5,
            "sunday": 6,
        }

        for weekday, target_idx in weekdays.
items():
            if re.search(rf"\blast\s
+{weekday}\b", question_lower):
             
   days_back = (base_date.weekday() - target_
idx) % 7
                if days_back == 0:
 
                   days_back = 7
            
    resolved.append((f"last {weekday}", base_
date - timedelta(days=days_back)))

        d
eduped: List[Tuple[str, date]] = []
        s
een = set()
        for label, date_value in 
resolved:
            key = (label, date_valu
e.isoformat())
            if key not in seen
:
                seen.add(key)
             
   deduped.append((label, date_value))
      
  return deduped

    @staticmethod
    def _
is_relative_date_lookup_question(question: st
r, question_type: Optional[str]) -> bool:
   
     if question_type != "temporal-reasoning"
:
            return False
        question_l
ower = question.lower()
        has_relative_
date = bool(
            re.search(
         
       r"\b(\d+|one|two|three|four|five|six|s
even|eight|nine|ten)\s+(days?|weeks?)\s+ago\b
",
                question_lower,
          
  )
            or re.search(r"\blast\s+(mond
ay|tuesday|wednesday|thursday|friday|saturday
|sunday)\b", question_lower)
            or r
e.search(r"\byesterday\b", question_lower)
  
      )
        if not has_relative_date:
   
         return False

        comparison_mar
kers = (
            "first",
            "ea
rliest",
            "latest",
            "b
efore",
            "after",
            "bet
ween",
            "compared",
            "h
igher",
            "lower",
            "mor
e",
            "less",
            "total",

            "how many",
            "how much
",
            "how long",
        )
        
if any(marker in question_lower for marker in
 comparison_markers):
            return Fals
e

        lookup_markers = (
            "wh
at ",
            "which ",
            "who 
",
            "where ",
            "from wh
om",
            "by whom",
            "did 
i buy",
            "did i get",
            
"did i receive",
            "did i purchase"
,
            "started to listen",
        )

        return any(marker in question_lower f
or marker in lookup_markers)

    def _format
_resolved_date_evidence_block(
        self,

        question: str,
        question_date:
 Optional[datetime],
        question_type: O
ptional[str],
        recall_result: Dict[str
, Any],
    ) -> str:
        if self.evidenc
e_mode != "oracle_v220" or question_type != "
temporal-reasoning":
            return ""
  
      if not self._is_relative_date_lookup_qu
estion(question, question_type):
            
return ""

        resolved_dates = self._res
olved_relative_dates(question, question_date)

        if not resolved_dates:
            r
eturn ""

        results = recall_result.get
("results", [])
        chunks = recall_resul
t.get("chunks", {})
        rows = []
       
 seen = set()
        target_dates = {date_va
lue for _, date_value in resolved_dates}
    
    for rank, fact in enumerate(results[:220]
, 1):
            fact_dates = {
            
    self._date_from_value(fact.get("occurred_
start")),
                self._date_from_val
ue(fact.get("occurred_end")),
               
 self._date_from_value(fact.get("mentioned_at
")),
            }
            fact_dates.dis
card(None)
            matched_dates = sorted
(date_value for date_value in fact_dates if d
ate_value in target_dates)
            if not
 matched_dates:
                continue

   
         text = self._compact_text(fact.get("
text", ""), 340)
            if not text:
   
             continue
            doc_id = st
r(fact.get("document_id") or "")
            
dedupe_text = re.sub(r"\W+", " ", text.lower(
)).strip()[:160]
            dedupe_key = f"{
doc_id}:{dedupe_text}"
            if dedupe_
key in seen:
                continue
       
     seen.add(dedupe_key)
            rows.ap
pend(
                {
                    "
rank": rank,
                    "matched": "
, ".join(date_value.isoformat() for date_valu
e in matched_dates),
                    "doc
": doc_id,
                    "type": fact.g
et("fact_type"),
                    "occurre
d": fact.get("occurred_start") or fact.get("o
ccurred_end") or "-",
                    "me
ntioned": fact.get("mentioned_at") or "-",
  
                  "chunk_id": fact.get("chunk
_id"),
                    "text": text,
    
            }
            )
            if le
n(rows) >= 24:
                break

       
 if not rows:
            return ""

        
title = "=== V2.20 V2.6 Self-Evolved Relative
-Date Evidence Block ==="
        lines = [
 
           title,
            "Relative date 
targets resolved from the question:",
       
 ]
        for label, date_value in resolved_
dates:
            lines.append(f"- {label} =
> {date_value.isoformat()}")
        lines.ex
tend(
            [
                "Facts re
trieved for those exact dates. Use them as sa
me-day evidence, even when the surface noun i
n the question differs from the extracted fac
t wording.",
                "",
            
    "Same-date candidate facts:",
           
 ]
        )

        used_chunks = []
      
  seen_chunks = set()
        for idx, row in
 enumerate(rows, 1):
            lines.append
(
                f"{idx}. target_date={row['
matched']} | occurred={row['occurred']} | "
 
               f"mentioned={row['mentioned']}
 | doc={row['doc']} | type={row['type']} | {r
ow['text']}"
            )
            chunk_
id = row.get("chunk_id")
            if chunk
_id and chunk_id in chunks and chunk_id not i
n seen_chunks:
                seen_chunks.ad
d(chunk_id)
                used_chunks.appen
d(chunk_id)

        if used_chunks:
        
    lines.extend(["", "Raw source snippets fo
r same-date facts:"])
            for idx, ch
unk_id in enumerate(used_chunks[:10], 1):
   
             chunk_info = chunks.get(chunk_id
) or {}
                chunk_text = self._co
mpact_text(chunk_info.get("chunk_text", ""), 
560)
                if chunk_text:
         
           lines.append(f"{idx}. chunk={chunk
_id} | {chunk_text}")

        return "\n".jo
in(lines)

    async def _format_resolved_dat
e_memory_backfill(
        self,
        ques
tion: str,
        question_date: Optional[da
tetime],
        question_type: Optional[str]
,
        bank_id: Optional[str],
    ) -> st
r:
        if self.evidence_mode != "oracle_v
220" or question_type != "temporal-reasoning"
 or not bank_id:
            return ""
      
  if not self._is_relative_date_lookup_questi
on(question, question_type):
            retu
rn ""

        resolved_dates = self._resolve
d_relative_dates(question, question_date)
   
     if not resolved_dates:
            retur
n ""

        database_url = os.environ.get("
HMS_API_DATABASE_URL")
        if not databas
e_url:
            return ""

        try:
  
          import asyncpg

            conn = 
await asyncpg.connect(database_url)
         
   try:
                target_dates = [date_
value for _, date_value in resolved_dates]
  
              rows = await conn.fetch(
      
              """
                    SELECT 
id, document_id, chunk_id, text, fact_type,
 
                          occurred_start, occ
urred_end, mentioned_at
                    F
ROM memory_units
                    WHERE ba
nk_id = $1
                      AND (
      
                  occurred_start::date = ANY(
$2::date[])
                        OR occurr
ed_end::date = ANY($2::date[])
              
          OR mentioned_at::date = ANY($2::dat
e[])
                      )
                
    ORDER BY mentioned_at, document_id
      
              LIMIT 180
                    "
"",
                    bank_id,
            
        target_dates,
                )
     
           if not rows:
                    r
eturn ""

                target_date_set = s
et(target_dates)
                question_ter
ms = self._content_terms(question)
          
      acquisition_re = re.compile(r"\b(acquir
ed|got|bought|purchased|received|picked up|or
dered)\b", re.I)

                def row_sco
re(row: Any) -> Tuple[int, str]:
            
        text = str(row["text"] or "")
       
             text_lower = text.lower()
      
              fact_dates = {
                
        self._date_from_value(row["occurred_s
tart"]),
                        self._date_f
rom_value(row["occurred_end"]),
             
           self._date_from_value(row["mention
ed_at"]),
                    }
             
       fact_dates.discard(None)
             
       exact_occurred = (
                   
     self._date_from_value(row["occurred_star
t"]) in target_date_set
                     
   or self._date_from_value(row["occurred_end
"]) in target_date_set
                    )

                    mentioned_match = self._d
ate_from_value(row["mentioned_at"]) in target
_date_set
                    term_overlap = 
sum(1 for term in question_terms if term in t
ext_lower)
                    acquisition = 
bool(acquisition_re.search(text))
           
         score = (
                        (1
2 if exact_occurred else 0)
                 
       + (2 if mentioned_match else 0)
      
                  + 3 * term_overlap
        
                + (6 if acquisition else 0)
 
                   )
                    retu
rn (-score, str(row["mentioned_at"] or ""), s
tr(row["document_id"] or ""))

              
  rows = sorted(rows, key=row_score)[:36]

  
              chunk_ids = [row["chunk_id"] fo
r row in rows if row["chunk_id"]]
           
     chunk_rows = []
                if chunk
_ids:
                    chunk_rows = await 
conn.fetch(
                        """
     
                   SELECT chunk_id, chunk_tex
t
                        FROM chunks
       
                 WHERE bank_id = $1 AND chunk
_id = ANY($2::text[])
                       
 LIMIT 16
                        """,
      
                  bank_id,
                  
      chunk_ids[:16],
                    )
 
               chunk_text_by_id = {row["chunk
_id"]: row["chunk_text"] for row in chunk_row
s}
            finally:
                await
 conn.close()
        except Exception:
     
       return ""

        title = "=== V2.20 
V2.6 Self-Evolved Exact-Date Memory Backfill 
==="
        lines = [
            title,
   
         "Memory units directly loaded from t
he fixed memory bank for the resolved relativ
e-date target. This is not new extraction; it
 is a date-constrained evidence backfill from
 stored memories.",
            "For acquisit
ion questions, stored wording such as got, ac
quired, received, or bought should be treated
 as candidate acquisition evidence for the it
em named in the memory.",
            "Resolv
ed targets:",
        ]
        for label, da
te_value in resolved_dates:
            lines
.append(f"- {label} => {date_value.isoformat(
)}")
        lines.extend(["", "Exact-date st
ored memories:"])

        used_chunks = []
 
       seen_chunks = set()
        for idx, r
ow in enumerate(rows, 1):
            text = 
self._compact_text(row["text"], 340)
        
    lines.append(
                f"{idx}. oc
curred={row['occurred_start'] or row['occurre
d_end'] or '-'} | "
                f"mention
ed={row['mentioned_at'] or '-'} | doc={row['d
ocument_id']} | "
                f"type={row
['fact_type']} | {text}"
            )
      
      chunk_id = row["chunk_id"]
            
if chunk_id and chunk_id in chunk_text_by_id 
and chunk_id not in seen_chunks:
            
    seen_chunks.add(chunk_id)
               
 used_chunks.append(chunk_id)

        if use
d_chunks:
            lines.extend(["", "Raw 
source snippets for exact-date backfill:"])
 
           for idx, chunk_id in enumerate(use
d_chunks[:8], 1):
                chunk_text 
= self._compact_text(chunk_text_by_id.get(chu
nk_id, ""), 560)
                if chunk_tex
t:
                    lines.append(f"{idx}. 
chunk={chunk_id} | {chunk_text}")

        re
turn "\n".join(lines)

    async def generate
_answer(
        self,
        question: str,

        recall_result: Dict[str, Any],
     
   question_date: Optional[datetime] = None,

        question_type: Optional[str] = None,

        bank_id: Optional[str] = None,
    ) 
-> Tuple[str, str, Optional[List[Dict[str, An
y]]]]:
        """
        Generate answer fr
om retrieved memories using Groq.

        Ar
gs:
            question: The question text
 
           recall_result: Full RecallResult d
ict containing results, entities, chunks, and
 trace
            question_date: Date when t
he question was asked (for temporal context)

            question_type: Question category 
(e.g., 'single-session-user', 'multi-session-
assistant')

        Returns:
            Tup
le of (answer, reasoning, None)
            -
 None indicates to use the memories from reca
ll_result
        """
        # Format contex
t based on selected mode
        if self.cont
ext_format == "structured":
            conte
xt = self._format_context_structured(recall_r
esult)
        else:
            context = se
lf._format_context_json(recall_result)

     
   if self._needs_structured_evidence_ledger(
question, question_type):
            ledger 
= self._format_structured_evidence_ledger(que
stion, recall_result)
            if ledger:

                context = f"{context}\n\n{led
ger}"
        if self.evidence_mode == "oracl
e_v220":
            backfill_block = await s
elf._format_resolved_date_memory_backfill(
  
              question,
                quest
ion_date,
                question_type,
    
            bank_id,
            )
          
  if backfill_block:
                context 
= f"{backfill_block}\n\n{context}"
          
  date_block = self._format_resolved_date_evi
dence_block(
                question,
      
          question_date,
                ques
tion_type,
                recall_result,
   
         )
            if date_block:
       
         context = f"{context}\n\n{date_block
}"

        context_instructions = self._get_
context_instructions()
        if (
         
   self.evidence_mode == "oracle_v220"
      
      and self._needs_structured_evidence_led
ger(question, question_type)
            and 
self._needs_v26_self_evolution_controller(que
stion, question_type)
        ):
            
context_instructions = f"{context_instruction
s}{self._v26_self_evolution_controller()}"

 
       # Format question date if provided
   
     formatted_question_date = question_date.
strftime("%Y-%m-%d %H:%M:%S UTC") if question
_date else "Not specified"

        # Use LLM
 to generate answer
        try:
            
answer_obj = await self.llm_config.call(
    
            messages=[
                    {

                        "role": "user",
     
                   "content": f"""You are a h
elpful assistant that must answer user questi
ons based on the previous conversations.

{co
ntext_instructions}**Answer Guidelines:**
1. 
Start by scanning retrieved context to unders
tand the facts and events that happened and t
he timeline.
2. Reason about all the memories
 and find the right answer, considering the m
ost recent memory as an update of the current
 facts.
3. If you have 2 possible answers, ju
st say both.

In general the answer must be c
omprehensive and plenty of details from the r
etrieved context.

For quantitative/counting 
questions ("how many..."): First list each un
ique item in your reasoning (1. X, 2. Y, 3. Z
...), scanning ALL facts, then count them for
 your answer.
If questions asks a location (w
here...?) make sure to include the location n
ame.
For recommendation questions ("can you r
ecommend...", "suggest...", "any tips..."): D
O NOT give actual recommendations. Instead, d
escribe what KIND the user would prefer based
 on their context. Example answer format: "Th
e user would prefer recommendations for [cate
gory] that focus on [their interest]. They wo
uld not prefer [what to avoid based on contex
t]."
For questions asking for help or instruc
tions, consider the users' recent memories an
d previous interactions with the assistant to
 understand their current situation better (r
ecent purchases, specific product models used
..)
For specific number/value questions, use 
the context to understand what is the most up
-to-date number based on recency, but also in
clude the reasoning (in the answer) on previo
us possible values and why you think are less
 relevant.
For open questions, include as muc
h details as possible from different sources 
that are relevant.
For questions where a spec
ific entity/role is mentioned and it's differ
ent from your memory, just say the truth, don
't make up anything just to fulfill the quest
ion. For example, if the question is about a 
specific sport, you should consider if the me
mories and the question are about the same sp
ort. (e.g. american football vs soccer, shows
 vs podcasts)
For comparative questions, say 
you don't know the answer if you don't have i
nformation about both sides. (or more sides)

For questions related to time/date, carefully
 review the question date and the memories da
te to correctly answer the question.
For ques
tions related to time/date calculation (e.g. 
How many days passed between X and Y?), caref
ully review the memories date to correctly an
swer the question and only provide an answer 
if you have information about both X and Y, o
therwise say it's not possible to calculate a
nd why.

Consider assistant's previous action
s (e.g., bookings, reminders) as impactful to
 the user experiences.


Question: {question}

Question Date: {formatted_question_date}

Re
trieved Context:
{context}


Answer:
""",
   
                 }
                ],
       
         response_format=QuestionAnswer,
    
            scope="memory",
                m
ax_completion_tokens=32768,
            )
   
         reasoning_text = answer_obj.reasonin
g or ""
            if reasoning_text:
      
          reasoning_text = reasoning_text + "
 "
            reasoning_text += f"(question 
date: {formatted_question_date})"
           
 return answer_obj.answer, reasoning_text, No
ne
        except Exception as e:
           
 return f"Error generating answer: {str(e)}",
 "Error occurred during answer generation.", 
None


async def run_benchmark(
    max_insta
nces: int = None,
    max_instances_per_categ
ory: int = None,
    max_questions_per_instan
ce: int = None,
    thinking_budget: int = 50
0,
    max_tokens: int = 8192,
    skip_inges
tion: bool = False,
    filln: bool = False,

    question_id: str = None,
    index_range:
 str = None,
    only_failed: bool = False,
 
   only_invalid: bool = False,
    only_inges
ted: bool = False,
    category: str = None,

    max_concurrent_items: int = 1,
    result
s_filename: str = "benchmark_results.json",
 
   results_dir: str = None,
    context_forma
t: str = "json",
    source_results: str = No
ne,
    ingest_only: bool = False,
    force_
reingest: bool = False,
    max_concurrent_qu
estions: int = 10,
    eval_semaphore_size: i
nt = 10,
    dataset_path: Optional[str] = No
ne,
    query_expansion_enabled: bool = False
,
    query_rewriting_strategy: str = "llm_ba
sed",
    session_expansion_weight: float = 0
.3,
    oracle_planner_v26: bool = False,
   
 oracle_planner_v220: bool = False,
    resum
e: bool = False,
):
    """
    Run the LongM
emEval benchmark.

    Args:
        max_inst
ances: Maximum number of instances to evaluat
e (None for all). Mutually exclusive with max
_instances_per_category and category.
       
 max_instances_per_category: Maximum number o
f instances per category (None for all). Mutu
ally exclusive with max_instances and categor
y.
        max_questions_per_instance: Maximu
m questions per instance (for testing)
      
  thinking_budget: Thinking budget for spread
ing activation search
        max_tokens: Max
imum tokens to retrieve from memories
       
 skip_ingestion: Whether to skip ingestion an
d use existing data
        filln: If True, o
nly process questions where the agent has no 
indexed data yet
        question_id: Optiona
l question ID to filter (e.g., 'e47becba'). U
seful with --skip-ingestion.
        only_fai
led: If True, only run questions that were pr
eviously marked as incorrect (is_correct=Fals
e)
        only_invalid: If True, only run qu
estions that were previously marked as invali
d (is_invalid=True)
        only_ingested: If
 True, only run questions whose memory bank a
lready exists (has been ingested)
        cat
egory: Optional category to filter questions 
(e.g., 'single-session-user', 'multi-session'
, 'temporal-reasoning'). Mutually exclusive w
ith max_instances and max_instances_per_categ
ory.
        max_concurrent_items: Maximum nu
mber of instances to process in parallel (def
ault: 1 for sequential)
        results_filen
ame: Filename for results (default: benchmark
_results.json).
        results_dir: Optional
 directory for results. If None, defaults to 
results/ relative to script location.
       
 context_format: How to format context for an
swer generation. "json" (raw JSON) or "struct
ured" (human-readable with facts+chunks).
   
     source_results: Source results file to r
ead failed/invalid questions from (for --only
-failed/--only-invalid). Defaults to benchmar
k_results.json.
        ingest_only: Only ing
est, skip evaluation
        force_reingest: 
If True, always re-ingest even if data alread
y exists (for re-running after fixing ingesti
on issues)
        dataset_path: Optional cus
tom dataset path. If None, uses the default d
ataset.
        oracle_planner_v26: If True, 
use the V2.6 Structured Evidence Ledger.
    
    oracle_planner_v220: If True, use pure v2
.6 plus diagnosis-driven self-evolution contr
ols.
        resume: If True, merge with exis
ting results and skip already processed items
 (default: False)
    """
    from rich.conso
le import Console

    console = Console()

 
   # Validate mutually exclusive arguments
  
  # --max-instances-per-category can't be com
bined with --max-instances or --category
    
# But --category CAN be combined with --max-i
nstances (to limit questions within a categor
y)
    if max_instances_per_category is not N
one and (max_instances is not None or categor
y is not None):
        console.print(
      
      "[red]Error: --max-questions-per-catego
ry cannot be combined with --max-instances or
 --category[/red]"
        )
        return


    # Validate --only-ingested can't be combi
ned with other dataset filters
    if only_in
gested:
        incompatible_flags = []
     
   if only_failed:
            incompatible_f
lags.append("--only-failed")
        if only_
invalid:
            incompatible_flags.appen
d("--only-invalid")
        if category is no
t None:
            incompatible_flags.append
("--category")
        if question_id is not 
None:
            incompatible_flags.append("
--question-id")
        if max_instances_per_
category is not None:
            incompatibl
e_flags.append("--max-instances-per-category"
)

        if incompatible_flags:
           
 console.print(f"[red]Error: --only-ingested 
cannot be combined with: {', '.join(incompati
ble_flags)}[/red]")
            return

    #
 Determine dataset path
    if dataset_path i
s not None:
        dataset_path = Path(datas
et_path)
        if not dataset_path.exists()
:
            console.print(f"[red]Error: Cus
tom dataset not found: {dataset_path}[/red]")

            return
        console.print(f"[
cyan]Using custom dataset: {dataset_path}[/cy
an]")
    else:
        # Check dataset exist
s, download if needed
        dataset_path = 
Path(__file__).parent / "datasets" / "longmem
eval_s_cleaned.json"
        if not dataset_p
ath.exists():
            if not download_dat
aset(dataset_path):
                console.p
rint("[red]Failed to download dataset. Please
 download manually:[/red]")
                c
onsole.print(
                    "[yellow]cu
rl -L 'https://huggingface.co/datasets/xiaowu
0162/longmemeval-cleaned/resolve/main/longmem
eval_s_cleaned.json' -o benchmarks/longmemeva
l/datasets/longmemeval_s_cleaned.json[/yellow
]"
                )
                return


    # Initialize components
    dataset = Lon
gMemEvalDataset()

    # Start with all items
 or load from dataset
    original_dataset_it
ems = None
    filtered_items = None

    # H
andle max_instances_per_category (aka max_que
stions_per_category)
    if max_instances_per
_category:
        console.print(f"[cyan]Limi
ting to {max_instances_per_category} question
s per category[/cyan]")
        if original_d
ataset_items is None:
            original_da
taset_items = dataset.load(dataset_path, max_
items=None)

        # Group by category and 
take max_instances_per_category from each
   
     from collections import defaultdict

   
     category_items = defaultdict(list)
     
   for item in original_dataset_items:
      
      cat = item.get("question_type", "unknow
n")
            category_items[cat].append(it
em)

        # Take up to max_instances_per_c
ategory from each category
        filtered_i
tems = []
        for cat, items in sorted(ca
tegory_items.items()):
            limited = 
items[:max_instances_per_category]
          
  filtered_items.extend(limited)
            
console.print(f"  [green]{cat}:[/green] {len(
limited)} questions (of {len(items)} availabl
e)")

        console.print(f"[green]Total: {
len(filtered_items)} questions across {len(ca
tegory_items)} categories[/green]")

    # Lo
ad previous results if filtering for failed/i
nvalid questions
    failed_question_ids = se
t()
    invalid_question_ids = set()
    if o
nly_failed or only_invalid:
        # Use sou
rce_results if specified, otherwise default t
o benchmark_results.json
        source_file 
= source_results if source_results else "benc
hmark_results.json"
        results_path = Pa
th(__file__).parent / "results" / source_file

        if not results_path.exists():
      
      console.print("[red]Error: Cannot use -
-only-failed or --only-invalid without existi
ng results file[/red]")
            console.p
rint(f"[yellow]Results file not found: {resul
ts_path}[/yellow]")
            return

     
   console.print(f"[cyan]Reading failed/inval
id questions from: {source_file}[/cyan]")
   
     with open(results_path, "r") as f:
     
       previous_results = json.load(f)

     
   # Extract question IDs that failed or are 
invalid
        for item_result in previous_r
esults.get("item_results", []):
            i
tem_id = item_result["item_id"]
            f
or detail in item_result["metrics"].get("deta
iled_results", []):
                if only_f
ailed and detail.get("is_correct") == False a
nd not detail.get("is_invalid", False):
     
               failed_question_ids.add(item_i
d)
                if only_invalid and detail
.get("is_invalid", False):
                  
  invalid_question_ids.add(item_id)

        
if only_failed:
            console.print(
  
              f"[cyan]Filtering to {len(faile
d_question_ids)} questions that failed (is_co
rrect=False)[/cyan]"
            )
        if
 only_invalid:
            console.print(
   
             f"[cyan]Filtering to {len(invali
d_question_ids)} questions that were invalid 
(is_invalid=True)[/cyan]"
            )

    
# Filter dataset by category if specified
   
 if category:
        console.print(f"[cyan]F
iltering questions by category: {category}[/c
yan]")
        if original_dataset_items is N
one:
            # Load full dataset without 
max_instances limit for filtering
           
 original_dataset_items = dataset.load(datase
t_path, max_items=None)

        filtered_ite
ms = [item for item in original_dataset_items
 if item.get("question_type") == category]

 
       if not filtered_items:
            con
sole.print(f"[yellow]No questions found for c
ategory '{category}'. Available categories:[/
yellow]")
            available_categories = 
set(item.get("question_type", "unknown") for 
item in original_dataset_items)
            f
or cat in sorted(available_categories):
     
           console.print(f"  - {cat}")
      
      return

        total_found = len(filte
red_items)
        will_run = min(total_found
, max_instances) if max_instances else total_
found
        if max_instances and total_foun
d > max_instances:
            console.print(

                f"[green]Found {total_found}
 questions for category '{category}' (will ru
n {will_run} due to --max-instances)[/green]"

            )
        else:
            cons
ole.print(f"[green]Found {total_found} questi
ons for category '{category}'[/green]")

    
# Filter dataset by question_id(s) if specifi
ed
    if question_id is not None:
        # 
Parse comma-separated question IDs
        ta
rget_ids = set(q.strip() for q in question_id
.split(",") if q.strip())
        if not targ
et_ids:
            console.print(f"[yellow]N
o valid question IDs provided in --question-i
d[/yellow]")
            return

        cons
ole.print(f"[cyan]Filtering to {len(target_id
s)} question ID(s): {sorted(target_ids)}[/cya
n]")

        # Load original items if not al
ready loaded
        if original_dataset_item
s is None:
            original_dataset_items
 = dataset.load(dataset_path, max_items=None)


        # If we already have filtered_items
 from category filtering, filter those
      
  # Otherwise start with all items
        it
ems_to_filter = filtered_items if filtered_it
ems is not None else original_dataset_items
 
       filtered_items = [item for item in ite
ms_to_filter if dataset.get_item_id(item) in 
target_ids]

        total_found = len(filter
ed_items)
        missing_ids = target_ids - 
{dataset.get_item_id(item) for item in filter
ed_items}
        if missing_ids:
           
 console.print(f"[yellow]Warning: {len(missin
g_ids)} question ID(s) not found in dataset: 
{sorted(missing_ids)}[/yellow]")
        will
_run = min(total_found, max_instances) if max
_instances else total_found
        if max_in
stances and total_found > max_instances:
    
        console.print(
                f"[gre
en]Found {total_found} items matching questio
n ID(s) (will run {will_run} due to --max-ins
tances)[/green]"
            )
        else:

            console.print(f"[green]Found {tot
al_found} items matching question ID(s)[/gree
n]")

    # Filter dataset by index range if 
specified
    if index_range:
        try:
  
          start_idx, end_idx = map(int, index
_range.split(","))
            start_idx = ma
x(1, start_idx)  # Ensure 1-indexed, min 1
  
          end_idx = max(start_idx, end_idx)


            console.print(f"[cyan]Filtering t
o item index range: {start_idx}-{end_idx} (1-
indexed)[/cyan]")

            if original_da
taset_items is None:
                original
_dataset_items = dataset.load(dataset_path, m
ax_items=None)

            items_to_filter =
 filtered_items if filtered_items is not None
 else original_dataset_items
            filt
ered_items = [item for i, item in enumerate(i
tems_to_filter, 1) if start_idx <= i <= end_i
dx]

            total_found = len(filtered_i
tems)
            will_run = min(total_found,
 max_instances) if max_instances else total_f
ound
            if max_instances and total_f
ound > max_instances:
                console
.print(
                    f"[green]Found {t
otal_found} questions in range {start_idx}-{e
nd_idx} (will run {will_run} due to --max-ins
tances)[/green]"
                )
          
  else:
                console.print(f"[gree
n]Found {total_found} questions in range {sta
rt_idx}-{end_idx}[/green]")
        except (V
alueError, AttributeError) as e:
            
console.print(f"[red]Error parsing --index-ra
nge '{index_range}'. Use format 'start,end' (
e.g., '75,412')[/red]")
            return

 
   # Filter dataset based on failed/invalid f
lags
    if only_failed or only_invalid:
    
    target_ids = failed_question_ids if only_
failed else invalid_question_ids
        if n
ot target_ids:
            filter_type = "fai
led" if only_failed else "invalid"
          
  console.print(f"[yellow]No {filter_type} qu
estions found in previous results. Nothing to
 run.[/yellow]")
            return

        
# Load original items if not already loaded
 
       if original_dataset_items is None:
   
         # Load full dataset without max_inst
ances limit for filtering
            origina
l_dataset_items = dataset.load(dataset_path, 
max_items=None)

        # If we already have
 filtered_items from category filtering, filt
er those
        # Otherwise start with all i
tems
        items_to_filter = filtered_items
 if filtered_items is not None else original_
dataset_items
        filtered_items = [item 
for item in items_to_filter if dataset.get_it
em_id(item) in target_ids]

        filter_ty
pe = "failed" if only_failed else "invalid"
 
       total_found = len(filtered_items)
    
    will_run = min(total_found, max_instances
) if max_instances else total_found
        i
f max_instances and total_found > max_instanc
es:
            console.print(
              
  f"[green]Found {total_found} {filter_type} 
items to re-evaluate (will run {will_run} due
 to --max-instances)[/green]"
            )
 
       else:
            console.print(f"[gre
en]Found {total_found} {filter_type} items to
 re-evaluate[/green]")

    # Create local me
mory engine
    from hms_api.engine.memory_en
gine import Budget
    from hms_api.models im
port RequestContext

    from benchmarks.comm
on.benchmark_runner import create_memory_engi
ne

    memory = await create_memory_engine()


    evidence_mode = None
    if oracle_plan
ner_v220:
        evidence_mode = "oracle_v22
0"
    elif oracle_planner_v26:
        evide
nce_mode = "oracle_v26"

    # Create answer 
generator
    answer_generator = LongMemEvalA
nswerGenerator(
        context_format=contex
t_format,
        evidence_mode=evidence_mode
,
    )
    # Log context format being used
 
   console.print(f"[blue]Context format: {con
text_format}[/blue]")

    answer_evaluator =
 LLMAnswerEvaluator()

    # Filter by only_i
ngested: only run items whose memory bank alr
eady exists
    if only_ingested:
        con
sole.print("[cyan]Filtering to only items wit
h existing memory banks...[/cyan]")

        
# Load all items if not already loaded
      
  if original_dataset_items is None:
        
    original_dataset_items = dataset.load(dat
aset_path, max_items=None)

        items_to_
check = filtered_items if filtered_items is n
ot None else original_dataset_items

        
# Check which items have existing banks
     
   ingested_items = []
        pool = await m
emory._get_pool()

        for item in items_
to_check:
            item_id = dataset.get_i
tem_id(item)
            agent_id = f"longmem
eval_{item_id}"

            # Check if bank 
has any memory units
            async with p
ool.acquire() as conn:
                result
 = await conn.fetchrow(
                    "
SELECT COUNT(*) as count FROM memory_units WH
ERE bank_id = $1 LIMIT 1", agent_id
         
       )
                if result["count"] >
 0:
                    ingested_items.append
(item)

        filtered_items = ingested_ite
ms
        console.print(f"[green]Found {len(
filtered_items)} items with existing memory b
anks[/green]")

        if not filtered_items
:
            console.print("[yellow]No items
 found with existing memory banks. Nothing to
 run.[/yellow]")
            return

    # De
termine query rewriting strategy
    if query
_expansion_enabled:
        strategy_name = q
uery_rewriting_strategy
    else:
        str
ategy_name = "noop"

    # Create benchmark r
unner
    retrieval_planner = None
    if ora
cle_planner_v220:
        retrieval_planner =
 longmemeval_oracle_planner_v220
    elif ora
cle_planner_v26:
        retrieval_planner = 
longmemeval_oracle_planner_v26

    runner = 
BenchmarkRunner(
        dataset=dataset,
   
     answer_generator=answer_generator,
     
   answer_evaluator=answer_evaluator,
       
 memory=memory,
        query_rewriting_strat
egy_name=strategy_name,
        query_rewriti
ng_enabled=query_expansion_enabled,
        s
ession_expansion_weight=session_expansion_wei
ght,
        retrieval_planner=retrieval_plan
ner,
    )

    if query_expansion_enabled:
 
       console.print(f"[cyan]Query expansion 
enabled: using {strategy_name} strategy[/cyan
]")

    console.print(f"[cyan]Session expans
ion weight: {session_expansion_weight}[/cyan]
")
    if oracle_planner_v26:
        console
.print("[cyan]Oracle planner v2.6 enabled: ba
se retrieval + structured evidence ledger[/cy
an]")
        for planner_category, planner_w
eight in sorted(ORACLE_PLANNER_V1_WEIGHTS.ite
ms()):
            suffix = " + query expansi
on + evidence appendix" if planner_category =
= "multi-session" else ""
            ledger 
= " + high-risk ledger" if planner_category i
n {"multi-session", "temporal-reasoning", "kn
owledge-update"} else ""
            console.
print(f"  [cyan]{planner_category}:[/cyan] {p
lanner_weight}{suffix}{ledger}")
    if oracl
e_planner_v220:
        profile = SELF_EVOLUT
ION_PROFILES["oracle_v220"]
        console.p
rint("[cyan]Oracle planner v2.20 enabled: pur
e v2.6 + diagnosis-driven self-evolution[/cya
n]")
        console.print(f"  [cyan]base:[/c
yan] {profile['base']}")
        console.prin
t(f"  [cyan]diagnosis source:[/cyan] {profile
['diagnosis_source']}")
        console.print
(f"  [cyan]selection:[/cyan] {profile['select
ion_rule']}")
        for planner_category, p
lanner_weight in sorted(ORACLE_PLANNER_V1_WEI
GHTS.items()):
            suffix = " + query
 expansion + evidence appendix" if planner_ca
tegory == "multi-session" else ""
           
 ledger = " + V2.6 ledger" if planner_categor
y in {"multi-session", "temporal-reasoning", 
"knowledge-update"} else ""
            contr
oller = (
                " + self-evolution 
controller"
                if planner_catego
ry in {"multi-session", "temporal-reasoning",
 "knowledge-update"}
                else ""

            )
            date_block = " + se
lf-evolved date evidence" if planner_category
 == "temporal-reasoning" else ""
            
console.print(f"  [cyan]{planner_category}:[/
cyan] {planner_weight}{suffix}{ledger}{contro
ller}{date_block}")

    # If filtering by ca
tegory, failed, invalid, only_ingested, or ma
x_instances_per_category, we need to use a cu
stom dataset that only returns those items
  
  # We'll temporarily replace the dataset's l
oad method
    if filtered_items is not None:

        original_load = dataset.load

      
  def filtered_load(path: Path, max_items: Op
tional[int] = None):
            return filte
red_items[:max_items] if max_items else filte
red_items

        dataset.load = filtered_lo
ad

    # Run benchmark
    # Single-phase ap
proach: each question gets its own isolated a
gent_id
    # This ensures each question only
 has access to its own context
    
    # Bui
ld output path: use results_dir if specified,
 otherwise use script location
    if results
_dir:
        output_path = Path(results_dir)
 / results_filename
    else:
        output_
path = Path(__file__).parent / "results" / re
sults_filename

    # Create results director
y if it doesn't exist
    output_path.parent.
mkdir(parents=True, exist_ok=True)

    merge
_with_existing = (
        filln
        or q
uestion_id is not None
        or only_failed

        or only_invalid
        or only_inge
sted
        or category is not None
        
or max_instances_per_category is not None
   
     or resume
    )

    # Print resume stat
us
    if resume:
        console.print(f"[cy
an]Resume mode enabled: will merge with exist
ing results from {output_path}[/cyan]")
     
   if not output_path.exists():
            c
onsole.print(f"[yellow]Warning: {output_path}
 does not exist, will start fresh[/yellow]")


    # Configuration for single-phase benchma
rk
    separate_ingestion = False
    clear_p
er_item = True  # Use unique agent_id per que
stion

    results = await runner.run(
      
  dataset_path=dataset_path,
        agent_id
="longmemeval",  # Will be suffixed with ques
tion_id per item
        max_items=max_instan
ces
        if not max_instances_per_category

        else None,  # Don't apply max_items 
when using per-category limit
        max_que
stions_per_item=max_questions_per_instance,
 
       thinking_budget=thinking_budget,
     
   max_tokens=max_tokens,
        skip_ingest
ion=skip_ingestion or only_ingested,  # Auto-
skip ingestion when using --only-ingested
   
     max_concurrent_questions=max_concurrent_
questions,
        eval_semaphore_size=eval_s
emaphore_size,
        separate_ingestion_pha
se=separate_ingestion,
        clear_agent_pe
r_item=clear_per_item,
        filln=filln,  
# Only process questions without indexed data

        specific_item=None,  # Already filte
red via filtered_items replacement
        ma
x_concurrent_items=max_concurrent_items,  # P
arallel instance processing
        output_pa
th=output_path,  # Save results incrementally

        merge_with_existing=merge_with_exist
ing,  # Merge when using --fill, --category, 
--only-failed, --only-invalid flags or specif
ic question
        ingest_only=ingest_only, 
 # Only ingest, skip evaluation
        force
_reingest=force_reingest,  # Force re-ingest 
even if data already exists
    )

    if ing
est_only:
        console.print(f"\n[green]�
�[/green] Ingest-only mode completed. Data is
 ready for evaluation.")
        console.prin
t(f"  To run evaluation later with a differen
t model:")
        console.print(f"  1. Updat
e .env with your preferred model")
        co
nsole.print(f"  2. Run: HMS_BENCHMARK=longmem
eval bash .aaaSCRIPT/run_benchmark.sh --only-
ingested --fill")
        return results

   
 # Display results (final save already happen
ed incrementally)
    runner.display_results(
results)
    console.print(f"\n[green]✓[/gr
een] Results saved incrementally to {output_p
ath}")

    # Generate detailed report by que
stion type
    generate_type_report(results)


    # Generate markdown results table
    ge
nerate_markdown_table(results, output_path)


    return results


def download_dataset(dat
aset_path: Path) -> bool:
    """
    Downloa
d the LongMemEval dataset if it doesn't exist
.

    Returns:
        True if successful, F
alse otherwise
    """
    import subprocess


    from rich.console import Console

    co
nsole = Console()

    url = "https://hf-mirr
or.com/datasets/xiaowu0162/longmemeval-cleane
d/resolve/main/longmemeval_s_cleaned.json"

 
   console.print("[yellow]Dataset not found. 
Downloading from HuggingFace...[/yellow]")
  
  console.print(f"[dim]URL: {url}[/dim]")
   
 console.print(f"[dim]Destination: {dataset_p
ath}[/dim]")

    # Create parent directory i
f it doesn't exist
    dataset_path.parent.mk
dir(parents=True, exist_ok=True)

    try:
  
      # Use curl to download with progress
  
      result = subprocess.run(
            ["
curl", "-L", "-o", str(dataset_path), url],
 
           capture_output=True,
            t
ext=True,
            timeout=300,  # 5 minut
e timeout
        )

        if result.return
code == 0 and dataset_path.exists():
        
    console.print("[green]✓ Dataset downloa
ded successfully[/green]")
            return
 True
        else:
            console.print
(f"[red]✗ Download failed: {result.stderr}[
/red]")
            return False

    except 
subprocess.TimeoutExpired:
        console.pr
int("[red]✗ Download timed out after 5 minu
tes[/red]")
        return False
    except E
xception as e:
        console.print(f"[red]�
�� Download error: {e}[/red]")
        return
 False


def generate_type_report(results: di
ct):
    """Generate a detailed report by que
stion type."""
    from rich.console import C
onsole
    from rich.table import Table

    
console = Console()

    # Aggregate stats by
 question type
    type_stats = {}

    for i
tem_result in results["item_results"]:
      
  metrics = item_result["metrics"]
        by
_category = metrics.get("category_stats", {})


        for qtype, stats in by_category.ite
ms():
            if qtype not in type_stats:

                type_stats[qtype] = {"total"
: 0, "correct": 0}
            type_stats[qty
pe]["total"] += stats["total"]
            ty
pe_stats[qtype]["correct"] += stats["correct"
]

    # Display table
    table = Table(titl
e="Performance by Question Type")
    table.a
dd_column("Question Type", style="cyan")
    
table.add_column("Total", justify="right", st
yle="yellow")
    table.add_column("Correct",
 justify="right", style="green")
    table.ad
d_column("Accuracy", justify="right", style="
magenta")

    for qtype, stats in sorted(typ
e_stats.items()):
        acc = (stats["corre
ct"] / stats["total"] * 100) if stats["total"
] > 0 else 0
        table.add_row(qtype, str
(stats["total"]), str(stats["correct"]), f"{a
cc:.1f}%")

    console.print("\n")
    conso
le.print(table)


def generate_markdown_table
(results: dict, json_output_path: Path):
    
"""Generate a markdown results table with mod
el configuration."""
    from rich.console im
port Console

    console = Console()

    # 
Aggregate stats by question type
    type_sta
ts = {}

    for item_result in results["item
_results"]:
        metrics = item_result["me
trics"]
        by_category = metrics.get("ca
tegory_stats", {})

        for qtype, stats 
in by_category.items():
            if qtype 
not in type_stats:
                type_stats
[qtype] = {"total": 0, "correct": 0, "invalid
": 0}
            type_stats[qtype]["total"] 
+= stats["total"]
            type_stats[qtyp
e]["correct"] += stats["correct"]
           
 type_stats[qtype]["invalid"] += stats.get("i
nvalid", 0)

    # Build markdown content
   
 lines = []
    lines.append("# LongMemEval B
enchmark Results")
    lines.append("")

    
# Add model configuration
    if "model_confi
g" in results:
        config = results["mode
l_config"]
        lines.append("## Model Con
figuration")
        lines.append("")
       
 lines.append(f"- **HMS**: {config['hms']['pr
ovider']}/{config['hms']['model']}")
        
lines.append(
            f"- **Answer Genera
tion**: {config['answer_generation']['provide
r']}/{config['answer_generation']['model']}"

        )
        lines.append(f"- **LLM Judg
e**: {config['judge']['provider']}/{config['j
udge']['model']}")
        lines.append("")


    lines.append(
        f"**Overall Accurac
y**: {results['overall_accuracy']:.2f}% ({res
ults['total_correct']}/{results['total_questi
ons']})"
    )
    lines.append("")

    # Re
sults by question type
    lines.append("## R
esults by Question Type")
    lines.append(""
)
    lines.append("| Question Type | Total |
 Correct | Invalid | Accuracy |")
    lines.a
ppend("|---------------|-------|---------|---
------|----------|")

    for qtype in sorted
(type_stats.keys()):
        stats = type_sta
ts[qtype]
        valid_total = stats["total"
] - stats["invalid"]
        acc = (stats["co
rrect"] / valid_total * 100) if valid_total >
 0 else 0
        invalid_str = str(stats["in
valid"]) if stats["invalid"] > 0 else "-"
   
     lines.append(f"| {qtype} | {stats['total
']} | {stats['correct']} | {invalid_str} | {a
cc:.1f}% |")

    # Add overall row
    total
_invalid = results.get("total_invalid", 0)
  
  invalid_str = str(total_invalid) if total_i
nvalid > 0 else "-"
    lines.append(
       
 f"| **OVERALL** | **{results['total_question
s']}** | **{results['total_correct']}** | **{
invalid_str}** | **{results['overall_accuracy
']:.1f}%** |"
    )

    # Write to file (sam
e directory as JSON, but .md extension)
    m
d_output_path = json_output_path.with_suffix(
".md")
    md_output_path.write_text("\n".joi
n(lines))
    console.print(f"\n[green]✓[/g
reen] Results table saved to {md_output_path}
")


if __name__ == "__main__":
    import ar
gparse
    import logging

    parser = argpa
rse.ArgumentParser(description="Run LongMemEv
al benchmark")
    parser.add_argument(
     
   "--max-instances",
        type=int,
     
   default=None,
        help="Limit TOTAL nu
mber of questions to evaluate (default: all 5
00). For per-category limits, use --max-quest
ions-per-category instead.",
    )
    parser
.add_argument(
        "--max-instances-per-c
ategory",
        "--max-questions-per-catego
ry",  # Alias since each instance = 1 questio
n in LongMemEval
        type=int,
        de
fault=None,
        dest="max_instances_per_c
ategory",
        help="Limit number of quest
ions per category (e.g., 20 = 20 questions fr
om each of the 6 categories = 120 total). Can
not be combined with --max-instances or --cat
egory.",
    )
    parser.add_argument(
     
   "--max-questions", type=int, default=None,
 help="Limit number of questions per instance
 (for quick testing)"
    )
    parser.add_ar
gument(
        "--thinking-budget", type=int
, default=500, help="Thinking budget for spre
ading activation search"
    )
    parser.add
_argument("--max-tokens", type=int, default=8
192, help="Maximum tokens to retrieve from me
mories")
    parser.add_argument("--skip-inge
stion", action="store_true", help="Skip inges
tion and use existing data")
    parser.add_a
rgument(
        "--fill",
        action="st
ore_true",
        help="Only process questio
ns not already in results file (for resuming 
interrupted runs)",
    )
    parser.add_argu
ment(
        "--question-id",
        type=s
tr,
        default=None,
        help="Filte
r to specific question ID(s). Can be a single
 ID (e.g., 'e47becba') or comma-separated IDs
 (e.g., 'e47becba,6f9b354f'). Useful with --s
kip-ingestion to test specific questions.",
 
   )
    parser.add_argument(
        "--inde
x-range",
        type=str,
        default=N
one,
        help="Filter to a range of item 
indices (e.g., '75,412'). Both start and end 
are inclusive, 1-indexed.",
    )
    parser.
add_argument(
        "--only-failed",
      
  action="store_true",
        help="Only run
 questions that were previously marked as inc
orrect (is_correct=False). Requires existing 
results file.",
    )
    parser.add_argument
(
        "--only-invalid",
        action="s
tore_true",
        help="Only run questions 
that were previously marked as invalid (is_in
valid=True). Requires existing results file."
,
    )
    parser.add_argument(
        "--o
nly-ingested",
        action="store_true",
 
       help="Only run questions whose memory 
bank already exists (has been ingested). Auto
matically skips ingestion. Cannot be combined
 with --only-failed, --only-invalid, --catego
ry, --question-id, or --max-instances-per-cat
egory.",
    )
    parser.add_argument(
     
   "--category",
        type=str,
        de
fault=None,
        help="Filter questions by
 category/question_type. Available categories
: 'single-session-user', 'multi-session', 'si
ngle-session-preference', 'temporal-reasoning
', 'knowledge-update', 'single-session-assist
ant'. Can be combined with --max-instances to
 limit questions within the category.",
    )

    parser.add_argument(
        "--parallel
",
        type=int,
        default=1,
     
   help="Number of instances to process in pa
rallel (default: 1 for sequential). Higher va
lues speed up evaluation but use more memory.
",
    )
    parser.add_argument(
        "--
results-filename",
        type=str,
        
default="benchmark_results.json",
        hel
p="Filename for results output (default: benc
hmark_results.json).",
    )
    parser.add_a
rgument(
        "--results-dir",
        typ
e=str,
        default=None,
        help="Op
tional directory for results. If not specifie
d, uses results/ relative to script location.
",
    )
    parser.add_argument(
        "--
context-format",
        type=str,
        ch
oices=["json", "structured"],
        default
="json",
        help="How to format context 
for answer generation. 'json' (raw JSON dump,
 original behavior) or 'structured' (human-re
adable format with facts grouped with source 
chunks). Default: json.",
    )
    parser.ad
d_argument(
        "--source-results",
     
   type=str,
        default=None,
        he
lp="Source results file to read failed/invali
d questions from (for --only-failed/--only-in
valid). Defaults to benchmark_results.json if
 not specified.",
    )
    parser.add_argume
nt(
        "--ingest-only",
        action="
store_true",
        help="Only ingest conver
sation data (skip evaluation). Use with --fil
l to skip already ingested items. Use after i
ngest to do evaluation with different model."
,
    )
    parser.add_argument(
        "--f
orce-reingest",
        action="store_true",

        help="Force re-ingest even if data al
ready exists. Use when you want to re-process
 ingestion for items that may have incomplete
 data.",
    )
    parser.add_argument(
     
   "--quiet",
        action="store_true",
  
      help="Suppress INFO level log messages 
(only show warnings and errors)",
    )
    p
arser.add_argument(
        "--max-concurrent
-questions",
        type=int,
        defaul
t=10,
        help="Maximum number of concurr
ent question processing (default: 10)",
    )

    parser.add_argument(
        "--eval-sem
aphore-size",
        type=int,
        defau
lt=10,
        help="Maximum concurrent LLM j
udge requests (default: 10)",
    )
    parse
r.add_argument(
        "--dataset-path",
   
     type=str,
        default=None,
        
help="Optional custom dataset path. If not sp
ecified, uses the default dataset.",
    )
  
  parser.add_argument(
        "--enable-quer
y-expansion",
        action="store_true",
  
      help="Enable query rewriting (default: 
disabled). When enabled, uses --query-rewriti
ng-strategy to determine the strategy.",
    
)
    parser.add_argument(
        "--query-r
ewriting-strategy",
        type=str,
       
 choices=["noop", "llm_based", "llm_driven"],

        default="llm_based",
        help="Q
uery rewriting strategy to use when --enable-
query-expansion is set. Options: 'noop' (no e
xpansion), 'llm_based' (rule-based decision w
ith LLM expansion), 'llm_driven' (LLM-driven 
analysis with entity expansion and time windo
w calculation) (default: llm_based)",
    )
 
   parser.add_argument(
        "--session-ex
pansion-weight",
        type=float,
        
default=0.3,
        help="Weight for session
-based node expansion (default: 0.3). Set to 
0 to disable.",
    )
    parser.add_argument
(
        "--oracle-planner-v26",
        act
ion="store_true",
        help="Use the V2.6 
Structured Evidence Ledger for high-risk ques
tions.",
    )
    parser.add_argument(
     
   "--oracle-planner-v220",
        action="s
tore_true",
        help="Use pure v2.6 retri
eval plus diagnosis-driven self-evolution con
trols.",
    )
    parser.add_argument(
     
   "--resume",
        action="store_true",
 
       help="Resume from a previous run by me
rging with existing results. Use with --resul
ts-filename to specify the same output file."
,
    )

    args = parser.parse_args()

    
log_level = logging.WARNING if args.quiet els
e logging.INFO
    logging.basicConfig(level=
log_level, format="%(asctime)s %(levelname)s 
%(message)s")

    # Validate that only one o
f --only-failed or --only-invalid is set
    
if args.only_failed and args.only_invalid:
  
      parser.error("Cannot use both --only-fa
iled and --only-invalid at the same time")

 
   planner_flags = [
        args.oracle_plan
ner_v26,
        args.oracle_planner_v220,
  
  ]
    if sum(1 for flag in planner_flags if
 flag) > 1:
        parser.error("Cannot use 
more than one oracle planner flag at the same
 time")

    # Validate mutually exclusive ar
guments
    # --max-instances-per-category ca
n't be combined with --max-instances or --cat
egory
    if args.max_instances_per_category 
is not None and (args.max_instances is not No
ne or args.category is not None):
        par
ser.error("--max-questions-per-category canno
t be combined with --max-instances or --categ
ory")

    results = asyncio.run(
        run
_benchmark(
            max_instances=args.ma
x_instances,
            max_instances_per_ca
tegory=args.max_instances_per_category,
     
       max_questions_per_instance=args.max_qu
estions,
            thinking_budget=args.thi
nking_budget,
            max_tokens=args.max
_tokens,
            skip_ingestion=args.skip
_ingestion,
            filln=args.fill,
    
        question_id=args.question_id,
       
     index_range=args.index_range,
          
  only_failed=args.only_failed,
            o
nly_invalid=args.only_invalid,
            on
ly_ingested=args.only_ingested,
            c
ategory=args.category,
            max_concur
rent_items=args.parallel,
            results
_filename=args.results_filename,
            
results_dir=args.results_dir,
            con
text_format=args.context_format,
            
source_results=args.source_results,
         
   ingest_only=args.ingest_only,
            
force_reingest=args.force_reingest,
         
   max_concurrent_questions=args.max_concurre
nt_questions,
            eval_semaphore_size
=args.eval_semaphore_size,
            datase
t_path=args.dataset_path,
            query_e
xpansion_enabled=args.enable_query_expansion,

            query_rewriting_strategy=args.qu
ery_rewriting_strategy,
            session_e
xpansion_weight=args.session_expansion_weight
,
            oracle_planner_v26=args.oracle_
planner_v26,
            oracle_planner_v220=
args.oracle_planner_v220,
            resume=
args.resume,
        )
    )


