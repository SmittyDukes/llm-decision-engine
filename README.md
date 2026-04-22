## 🏀 LLM Decision Engine (Basketball Domain Example)

A governed LLM decision engine that enforces structured outputs, validation, and policy-based decision control for basketball decision-making scenarios.
This project demonstrates how to wrap large language models with validation, policy enforcement, and logging layers to create reliable decision systems rather than simple prompt-driven applications.

## 🔎 Example Decision

Input
Team is up 4, player has 3 fouls, fatigue index is 0.55, 2 minutes left.
Should we extend minutes?
Output
{
  "answer": "do_not_extend",
  "model_reason": "Player has 3 fouls with 2 minutes left, increasing the risk of fouling out. Fatigue is moderate and may reduce effectiveness.",
  "policy_reason": "confidence_above_threshold",
  "confidence": 0.85,
  "decision_type": "normal"
}

## 🚀 Overview
Most LLM applications rely purely on prompts and blindly trust model outputs.
This system demonstrates how to wrap LLMs in validation, policy, and logging layers to produce:
Structured, machine-readable outputs
Enforced response contracts
Policy-governed decisions
Abstention under uncertainty
Full decision traceability

### 👉 The result is a controlled decision pipeline, not just an LLM response.

## 💡 Why This Matters
LLMs are powerful but unreliable when used directly.
This project demonstrates how to move from:
prompt → response
to:
LLM → validation → policy → auditable decision system
This is the difference between:
demo-level AI
production-style AI systems

## 🧱 System Architecture
User Input
   ↓
Prompt (structured contract enforced)
   ↓
LLM (gpt-4.1-mini)
   ↓
Parser (JSON extraction + error handling)
   ↓
Validator (schema + type + domain checks)
   ↓
Decision Policy (abstain / override / accept)
   ↓
Logger (JSONL decision trace)
   ↓
Final Decision Output

## ▶️ How to Run
1. Clone the repository
git clone <repo-url>
cd <repo>
2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Add your OpenAI API key
Create a .env file:
OPENAI_API_KEY=your-key-here
5. Run the system
PYTHONPATH=. python3 app/main.py

## 🧪 System Guarantees
1. Structured Output Contract
The model must return:
{
  "answer": "extend | do_not_extend | abstain",
  "reason": "string",
  "confidence": 0.0 - 1.0
}
2. Validation Layer
The system rejects outputs that violate:
Missing required fields
Invalid data types
Invalid answer domain
Confidence outside [0,1]
Empty or meaningless reasoning
3. Decision Policy Layer
The system does not blindly trust the model.
Rules include:
Abstain if confidence is below threshold
Abstain if uncertainty is detected in reasoning
Override invalid high-confidence abstain
Reject weak or empty reasoning
4. Logging (Traceability)
Every decision is recorded as a JSONL event.
Example Log Entry
{
  "event_id": "f1183575-cf95-412f-9a77-ecc248c76f00",
  "timestamp": "2026-03-25T12:00:00Z",
  "request": {
    "question": "...",
    "structured": true
  },
  "raw_output": "...",
  "parsed_output": {
    "answer": "do_not_extend",
    "reason": "...",
    "confidence": 0.85
  },
  "decision": {
    "answer": "do_not_extend",
    "policy_reason": "confidence_above_threshold",
    "confidence": 0.85
  }
}
This enables:
debugging
auditing
reproducibility
evaluation

## 🧠 Key Engineering Decisions
Structured Output
LLMs are unreliable without constraints.
Enforcing JSON ensures predictable downstream processing.
Validation Layer
A syntactically valid response is not necessarily correct.
Validation enforces contract-level correctness.
Decision Policy
Separates:
model reasoning ≠ system decision
This enables:
governance
overrides
abstention logic
Logging
Without traceability, system behavior cannot be audited or improved.

## 🧠 RAG Architecture (v2)
This project has been upgraded from a prompt-only LLM pipeline to a Retrieval-Augmented Generation (RAG) system.
Offline Indexing (Build Time)
Basketball decision policies are stored as plain text documents.

Steps:

1. Documents are stored in app/data/

2. Documents are chunked into overlapping passages

3. Passages are embedded using OpenAI's text-embedding-3-small

4. Embeddings are stored in a FAISS vector index

5. Cosine similarity is used for retrieval

6. Runtime Retrieval (Per Request)

For each incoming question:

The question is embedded using the same model
The top-3 most semantically relevant policy chunks are retrieved
Retrieved chunks are injected into the LLM prompt
The model reasons using grounded policy context

Why RAG:

A prompt-only assistant generates answers from training data, which can:
hallucinate
drift from policy
produce inconsistent decisions
RAG grounds the model's reasoning in explicit knowledge.
Every decision can be traced back to retrieved policy documents.

## 📚 Knowledge Base

Policies are stored as text documents: app/data/

Documents include:


- foul_management.txt — foul threshold rules by quarter
- fatigue_policy.txt — minutes management and rest protocols
- substitution_rules.txt — timing and rotation depth rules
- game_situation_policy.txt — score margin and clutch time logic
- player_position_policy.txt — position-specific decision rules

## ⚠️ Limitations
Current system limitations:
No game-state awareness (clutch vs non-clutch)
No player-specific context (skill, matchup, role)
Static confidence thresholds
No automated evaluation harness yet

## 🚧 Future Improvements
Planned enhancements:
Game-state-aware decision policy
Evaluation framework (accuracy, calibration, failure analysis)
Confidence calibration improvements
Multi-agent or rule-based arbitration

## 🛠 Tech Stack
Python
OpenAI API
FAISS vector search
JSONL logging
Custom parser / validator / policy layers

## 🎯 What This Demonstrates
This project showcases:
End-to-end LLM system design
Structured output enforcement
Failure handling and validation
Decision governance architecture
Retrieval-augmented reasoning (RAG)
Production-style logging and traceability

## 🔥 Final Note
This is not a prompt demo.
This is a controlled LLM decision system designed for:
reliability
auditability
real-world deployment patterns
