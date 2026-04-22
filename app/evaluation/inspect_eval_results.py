
import json
from pathlib import Path

log_path = Path("logs/decision_logs.jsonl")
rows = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]

eval_rows = [r for r in rows if r.get("event_kind") == "eval"]
print(f"eval rows found: {len(eval_rows)}")

for r in eval_rows[-8:]:  # last run (8 prompts)
    grade = r.get("grade", {})
    status = grade.get("status")
    pid = r.get("prompt_id")
    failures = grade.get("failures", [])
    print(f"{pid:18} -> {status:4} {failures}")
PY