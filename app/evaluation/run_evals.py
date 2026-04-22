"""
Simple offline eval loop:
- load prompts
- run pipeline for each prompt
- grade each result
- log and print summary

Run:
    cd main && python -m app.evaluation.run_evals
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from uuid import uuid4

# `main/` must be on sys.path (parent of the `app` package).
_MAIN_DIR = Path(__file__).resolve().parents[2]
if str(_MAIN_DIR) not in sys.path:
    sys.path.insert(0, str(_MAIN_DIR))

from app.evaluation.grader import grade_response
from app.pipeline.logger import log_event

PROMPTS_PATH = Path(__file__).resolve().parent / "prompts.json"


def load_prompts() -> list[dict]:
    with open(PROMPTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def run_evals() -> None:
    # Keep this import inside the function because orchestrator builds the retriever index on import.
    from app.pipeline.orchestrator import ask_basketball_question

    prompts = load_prompts()

    total = len(prompts)
    passed = 0
    failed = 0

    for item in prompts:
        prompt_id = item["id"]
        prompt = item["prompt"]
        print(f"\nRunning eval: {prompt_id}")

        event = {
            "event_id": str(uuid4()),
            "event_kind": "eval",
            "prompt_id": prompt_id,
            "prompt": prompt,
        }

        # Single entry point: same path as the CLI (retrieve → LLM → parse → validate → policy → log).
        pipeline_result = ask_basketball_question(prompt, structured=True)
        event["pipeline_result"] = pipeline_result

        grade = grade_response(prompt_id, prompt, pipeline_result)
        event["grade"] = grade

        if grade["status"] == "pass":
            passed += 1
            print("  result: PASS")
        else:
            failed += 1
            print(f"  result: FAIL -> {grade.get('failures', [])}")

        log_event(event)

    print("\nEvaluation Summary")
    print("------------------")
    print(f"Total Prompts: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    run_evals()
