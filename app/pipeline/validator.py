from app.schemas.failure_types import FAILURE_TYPES

ALLOWED_ANSWERS = ["extend", "do_not_extend", "abstain"]

def validate_output(parsed: dict):
    # 0. Type guard
    if not isinstance(parsed, dict):
        return {
            "status": "fail",
            "failure_type": FAILURE_TYPES["FORMAT_DRIFT"],
            "reason": "Parsed output is not a dictionary"
        }
    # 1. Required fields
    required_fields = ["answer", "reason", "confidence"]
    for field in required_fields:
        if field not in parsed:
            return {
                "status": "fail",
                "failure_type": FAILURE_TYPES["FORMAT_DRIFT"],
                "reason": f"Missing: {field}"
            }

    # 2. Type checks
    if not isinstance(parsed["answer"], str):
        return {
            "status": "fail",
            "failure_type": FAILURE_TYPES["INVALID_TYPE"],
            "reason": "Answer must be a string"
        }

    if parsed["reason"] is None or not isinstance(parsed["reason"], str):
        return {
            "status": "fail",
            "failure_type": FAILURE_TYPES["INVALID_TYPE"],
            "reason": "Reason must be a string"
        }

    if not isinstance(parsed["confidence"], (int, float)):
        return {
            "status": "fail",
            "failure_type": FAILURE_TYPES["INVALID_TYPE"],
            "reason": "Confidence must be numeric"
        }

    # 3. Empty string check
    if not parsed["answer"].strip() or not parsed["reason"].strip():
        return {
            "status": "fail",
            "failure_type": FAILURE_TYPES["FORMAT_DRIFT"],
            "reason": "Answer or reason is empty"
        }

    # 4. Answer domain check
    if parsed["answer"] not in ALLOWED_ANSWERS:
        return {
            "status": "fail",
            "failure_type": FAILURE_TYPES["INVALID_TYPE"],
            "reason": f"Invalid answer: {parsed['answer']}"
        }

    # 5. Confidence bounds
    if not (0 <= parsed["confidence"] <= 1):
        return {
            "status": "fail",
            "failure_type": FAILURE_TYPES["INVALID_CONFIDENCE"],
            "reason": "Confidence must be between 0 and 1"
        }

    # PASS
    return {
        "status": "success",
        "data": parsed
    }