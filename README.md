🏀 LLM Basketball Decision System
A structured LLM-powered decision system that evaluates whether a basketball player’s minutes should be extended, with strict output validation, abstention logic, and full decision trace logging.
🚀 Overview
Most LLM applications return unstructured, unverifiable answers.
This system enforces:
Structured outputs (JSON contract)
Validation of model responses
Decision governance through policy rules
Abstention under uncertainty
Full traceability via logging
The result is a controlled decision pipeline, not just a model response.
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
⚙️ Example Usage
Ask a basketball question:
Team is up 4, player has 3 fouls, fatigue index is 0.55, 2 minutes left. Should we extend minutes?

Structured output? yes
📤 Example Output
{
  "answer": "do_not_extend",
  "model_reason": "Player has 3 fouls with 2 minutes left, increasing risk of fouling out. Fatigue is moderate, which may reduce effectiveness and increase defensive mistakes.",
  "policy_reason": "confidence_above_threshold",
  "confidence": 0.85,
  "decision_type": "normal"
}
▶️ How to Run
Clone the repo
Create a virtual environment:
python3 -m venv .venv && source .venv/bin/activate
Install dependencies:
pip install -r requirements.txt
Add your OpenAI API key to .env:
OPENAI_API_KEY=your-key-here
Run the system:
PYTHONPATH=. python3 app/main.py
🧪 What This System Enforces
1. Structured Output Contract
The model must return:
{
  "answer": "extend | do_not_extend | abstain",
  "reason": "string",
  "confidence": 0.0 - 1.0
}
2. Validation Layer
The system rejects outputs that violate:
Missing fields
Invalid types
Invalid answer domain
Confidence out of bounds
Empty reasoning
3. Decision Policy Layer
The system does not blindly trust the model.
Rules include:
Abstain if confidence < threshold
Abstain if uncertainty detected in reasoning
Override invalid high-confidence abstain
Reject weak or empty reasoning
4. Logging (Traceability)
Every decision is logged as a JSONL entry:
{
  "event_id": "...",
  "timestamp": "...",
  "request": {...},
  "raw_output": "...",
  "parsed_output": {...},
  "decision": {...},
  "retry": {...}
}
This enables:
debugging
auditing
evaluation
reproducibility
🧠 Key Engineering Decisions
Why structured output?
LLMs are unreliable when left unconstrained. A strict JSON contract ensures predictable downstream processing.
Why validation?
A syntactically correct response is not necessarily a valid decision. Validation enforces correctness beyond formatting.
Why a decision policy layer?
Separates:
model reasoning ≠ system decision
This allows:
governance
overrides
abstention logic
Why logging?
Without traceability, system behavior cannot be audited or improved.
⚠️ Limitations
No game-state awareness (e.g., clutch vs regular time)
No player-specific context (skill level, role)
Static decision thresholds
No evaluation harness yet
🚧 Future Improvements
Game-state-aware decision policy (clutch situations)
Evaluation framework (accuracy, calibration, failure analysis)
Confidence calibration improvements
Multi-agent or rule-based arbitration layer
🛠️ Tech Stack
Python
OpenAI API
JSONL logging
Custom validation + policy layers
🎯 What This Demonstrates
This project shows:
End-to-end system design
Controlled LLM usage (not just prompting)
Failure handling and retries
Decision governance
Production-style logging