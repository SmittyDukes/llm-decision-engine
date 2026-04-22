"""
Simple eval grader (junior-friendly pattern):
1) Check for pipeline errors
2) Run a short list of rule checks
3) Return pass/fail + failure tags
"""

from __future__ import annotations

import re


UNCERTAINTY_WORDS = [
    "not sure",
    "uncertain",
    "unclear",
    "may",
    "might",
    "could",
    "possibly",
    "unknown",
    "cannot determine",
    "insufficient",
]


def has_pipeline_error(result: dict) -> bool:
    return isinstance(result, dict) and "error_type" in result


def check_constraint_violation(prompt_id: str, answer: str) -> bool:
    # Missing critical info -> must abstain.
    if prompt_id in ("missing_fatigue", "missing_foul_info") and answer != "abstain":
        return True

    # 5 fouls -> should never extend.
    if prompt_id == "foul_trouble" and answer == "extend":
        return True

    return False


def check_hallucination(prompt: str, reason_text: str) -> bool:
    # Very lightweight check: fatigue-like decimals in reason that are not in prompt.
    for token in re.findall(r"\b0?\.\d{2,}\b|\b1\.0{1,}\b", reason_text):
        if token not in prompt:
            return True
    return False


def check_overconfident_uncertainty(confidence: float, reason_text: str) -> bool:
    if confidence < 0.85:
        return False
    reason_lower = reason_text.lower()
    return any(word in reason_lower for word in UNCERTAINTY_WORDS)


def grade_response(prompt_id: str, prompt: str, pipeline_result: dict) -> dict:
    failures = []

    if has_pipeline_error(pipeline_result):
        return {
            "status": "fail",
            "failures": ["PIPELINE_ERROR"],
            "detail": pipeline_result,
        }

    answer = str(pipeline_result.get("answer", "")).strip()
    reason_text = str(
        pipeline_result.get("model_reason") or pipeline_result.get("reason") or ""
    ).strip()

    try:
        confidence = float(pipeline_result.get("confidence", 0))
    except (TypeError, ValueError):
        confidence = 0.0

    if check_constraint_violation(prompt_id, answer):
        failures.append("CONSTRAINT_VIOLATION")

    if check_hallucination(prompt, reason_text):
        failures.append("HALLUCINATION")

    if check_overconfident_uncertainty(confidence, reason_text):
        failures.append("OVERCONFIDENT_UNCERTAINTY")

    if failures:
        return {"status": "fail", "failures": failures}

    return {"status": "pass"}
