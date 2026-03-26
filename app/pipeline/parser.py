import re
import json
from app.schemas.failure_types import FAILURE_TYPES




#CLEANER
def clean_json_response(raw: str) -> str:
    if not raw or not raw.strip():
        return ""
    raw = raw.strip()

    # Exact JSON inside ``` ``` if present
    fence_pattern = r"```(?:json)?\s*(.*?)\s*```"
    match = re.search(fence_pattern, raw, re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(1).strip()
    return raw

#PARSER
def parse_output(raw: str):
    if not isinstance(raw, str):
        return {
            "status": "fail",
            "failure_type": FAILURE_TYPES["FORMAT_DRIFT"],
            "error": "Raw output is not a string",
            "raw": None
        }

    cleaned = clean_json_response(raw)


    # Empty guard
    if not cleaned:
        return {
            "status": "fail",
            "failure_type": FAILURE_TYPES["EMPTY_OUTPUT"],
            "error": "Model returned empty response",
            "raw": raw
        }

    # JSON parse
    try:
        parsed = json.loads(cleaned)
    except Exception as e:
        return {
            "status": "fail",
            "failure_type": FAILURE_TYPES["FORMAT_DRIFT"],
            "error": str(e),
            "raw": cleaned
        }

    return {
        "status": "success",
        "data": parsed
    }