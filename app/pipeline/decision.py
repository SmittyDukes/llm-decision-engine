def apply_decision_policy(parsed_output):
    UNCERTAINTY_KEYWORDS = [
        "not sure",
        "uncertain",
        "insufficient information",
        "cannot determine",
        "unknown",
        "could be",
        "might be",
        "possibly"
    ]

    ABSTAIN_THRESHOLD = 0.6

    answer = parsed_output["answer"]
    reason = (parsed_output["reason"] or "").lower()
    confidence = parsed_output["confidence"]

    # --- Rule 1: Uncertainty detection ---
    if any(word in reason for word in UNCERTAINTY_KEYWORDS):
        return {
            "answer": "abstain",
            "model_reason": parsed_output["reason"],
            "reason": "model_expressed_uncertainty",
            "confidence": confidence,
            "decision_type": "abstained"
        }

    # --- Rule 2: Low confidence → abstain ---
    if confidence < ABSTAIN_THRESHOLD:
        return {
            "answer": "abstain",
            "model_reason": parsed_output["reason"],
            "reason": "confidence_below_threshold",
            "confidence": confidence,
            "decision_type": "abstained"
        }

    # --- Rule 3: Invalid abstain (high confidence + abstain) → override ---
    if answer == "abstain" and confidence >= ABSTAIN_THRESHOLD:
        return {
            "answer": "do_not_extend",  # conservative default
            "reason": "override_invalid_abstain_high_confidence",
            "confidence": confidence,
            "decision_type": "override"
        }


    # --- Rule 5: Weak/empty reasoning → abstain ---
    if not reason.strip():
        return {
            "answer": "abstain",
            "reason": "missing_reason",
            "confidence": confidence,
            "decision_type": "abstained"
        }

    # --- Default: accept ---
    return {
        "answer": answer,
        "model_reason": parsed_output["reason"],
        "reason": "confidence above threshold",
        "confidence": confidence,
        "decision_type": "normal"
    }