import uuid
from datetime import datetime, timezone

from app.llm.client import client
from app.pipeline.parser import parse_output
from app.pipeline.validator import validate_output
from app.pipeline.decision import apply_decision_policy
from app.pipeline.logger import log_event
from app.schemas.failure_types import FAILURE_TYPES
from retriever import build_index, retrieve  # ← NEW

# Build index once at startup
index, all_chunks = build_index()  # ← NEW


def ask_basketball_question(question: str, structured: bool = True):
    """
    End-to-end pipeline:
    Retrieve → LLM → Parse → Validate → Decision → Log
    """

    # --- RETRIEVE RELEVANT POLICY CHUNKS --- ← NEW
    retrieved_chunks = retrieve(question, index, all_chunks, k=3)
    context_block = "\n".join([
        f"[{i+1}] {chunk['source']}: {chunk['text']}"
        for i, chunk in enumerate(retrieved_chunks)
    ])

    # --- BUILD PROMPT ---
    instructions = (
        "You are a basketball decision-support assistant. "
        "Use the following retrieved policy context to ground your reasoning. "
        "If the context is relevant, prioritize it over general basketball knowledge. "
        "Answer clearly and do not invent facts.\n\n"
        f"--- Retrieved policy context ---\n{context_block}\n--- End context ---"  # ← NEW
    )

    if structured:
        prompt = f"""
    Return your answer as valid JSON with exactly these keys:
    - answer: one of ["extend", "do_not_extend", "abstain"]
    - reason: string
    - confidence: float between 0 and 1

    Question: {question}
    """
    else:
        prompt = question

    retry_attempted = False
    retry_success = None

    # --- LLM CALL ---
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=instructions,
            input=prompt,
            temperature=0.3,
        )
        raw = response.output_text
    except Exception as e:
        event = {
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request": {"question": question, "structured": structured},
            "error_type": FAILURE_TYPES["API_FAILURE"],
            "error_message": str(e),
        }
        log_event(event)
        return event

    # --- EMPTY GUARD ---
    if not raw or not raw.strip():
        event = {
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request": {"question": question, "structured": structured},
            "error_type": FAILURE_TYPES["EMPTY_OUTPUT"],
        }
        log_event(event)
        return event

    # --- PARSE ---
    parse_result = parse_output(raw)

    # --- RETRY IF PARSE FAILS ---
    if parse_result["status"] == "fail":
        retry_attempted = True

        try:
            response_retry = client.responses.create(
                model="gpt-4.1-mini",
                instructions=instructions,
                input=prompt,
                temperature=0.3,
            )
            raw_retry = client.call_llm(prompt)
            parse_result = parse_output(raw_retry)
            retry_success = parse_result["status"] == "success"

            if parse_result["status"] == "fail":
                event = {
                    "event_id": str(uuid.uuid4()),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "request": {"question": question, "structured": structured},
                    "raw_output": raw,
                    "error_type": parse_result["failure_type"],
                    "error_message": parse_result["error"],
                    "retry": {
                        "attempted": True,
                        "success": False
                    }
                }
                log_event(event)
                return event

        except Exception as e:
            event = {
                "event_id": str(uuid.uuid4()),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "request": {"question": question, "structured": structured},
                "error_type": FAILURE_TYPES["FORMAT_DRIFT"],
                "error_message": f"Retry failed: {str(e)}",
                "retry": {
                    "attempted": True,
                    "success": False
                }
            }
            log_event(event)
            return event

    # --- VALIDATE ---
    validate_result = validate_output(parse_result["data"])

    if validate_result["status"] == "fail":
        event = {
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request": {"question": question, "structured": structured},
            "raw_output": raw,
            "parsed_output": parse_result["data"],
            "error_type": validate_result["failure_type"],
            "error_message": validate_result["reason"],
        }
        log_event(event)
        return event

    # --- DECISION POLICY ---
    final_output = apply_decision_policy(validate_result["data"])

    # --- SUCCESS LOG ---
    event = {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),

        "request": {
            "question": question,
            "structured": structured
        },

        "model": {
            "name": "gpt-4.1-mini",
            "temperature": 0.3
        },

        "raw_output": raw,
        "parsed_output": validate_result["data"],
        "decision": final_output,

        "retrieved_chunks": [  # ← NEW — log what was retrieved
            {
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
                "score": chunk["score"]
            }
            for chunk in retrieved_chunks
        ],

        "retry": {
            "attempted": retry_attempted,
            "success": retry_success
        }
    }

    log_event(event)
    return final_output