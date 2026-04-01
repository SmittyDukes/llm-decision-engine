🏀 LLM Decision Engine (Basketball Domain Example)

A governed LLM decision engine that enforces structured outputs, validation, and policy-based decision control for basketball decision-making scenarios.
🔎 Example Decision
Input
Team is up 4, player has 3 fouls, fatigue index is 0.55, 2 minutes left. Should we extend minutes?
Output
{
  "answer": "do_not_extend",
  "model_reason": "Player has 3 fouls with 2 minutes left, increasing the risk of fouling out. Fatigue is moderate and may reduce effectiveness.",
  "policy_reason": "confidence_above_threshold",
  "confidence": 0.85,
  "decision_type": "normal"
}


🚀 Overview

Most LLM applications rely purely on prompts and trust model outputs.
This system demonstrates how to wrap LLMs in validation, policy, and logging layers to produce:
Structured, machine-readable outputs
Enforced response contracts
Policy-governed decisions (not blind model trust)
Abstention under uncertainty
Full decision traceability
👉 The result is a controlled decision pipeline, not just an LLM response.


💡 Why This Matters

LLMs are powerful but unreliable when used directly.
This project shows how to move from:
prompt → response
to:
LLM → validation → policy → auditable decision system
This is the difference between:
demo-level AI
production-ready AI systems


🧱 System Architecture

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


▶️ How to Run

Clone the repository
Create a virtual environment:
python3 -m venv .venv && source .venv/bin/activate
Install dependencies:
pip install -r requirements.txt
Add your OpenAI API key to .env:
OPENAI_API_KEY=your-key-here
Run the system:
PYTHONPATH=. python3 app/main.py

🧪 System Guarantees

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
Confidence outside [0, 1]
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
  "event_id": "f1183575-cf95-412f-9a77-ecc248c76f00"
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

🧠 Key Engineering Decisions

Structured Output
LLMs are unreliable without constraints. Enforcing JSON ensures predictable downstream processing.
Validation Layer
A syntactically valid response is not necessarily correct. Validation enforces contract-level correctness.
Decision Policy
Separates:
model reasoning ≠ system decision
This enables:
governance
overrides
abstention logic
Logging
Without traceability, system behavior cannot be audited or improved.

⚠️ Limitations

No game-state awareness (e.g., clutch vs non-clutch)
No player-specific context (skill, role, matchup)
Static confidence thresholds
No evaluation harness yet


🚧 Future Improvements

Game-state-aware decision policy (clutch scenarios)
Evaluation framework (accuracy, calibration, failure analysis)
Confidence calibration improvements
Multi-agent or rule-based arbitration
🛠️ Tech Stack
Python
OpenAI API
JSONL logging
Custom parser, validator, and policy layers


🎯 What This Demonstrates

This project showcases:
End-to-end LLM system design
Structured output enforcement
Failure handling and retries
Decision governance architecture
Production-style logging and traceability

🔥 Final note
This is not a prompt demo.
This is a controlled LLM decision system designed for reliability, auditability, and real-world deployment patterns.
