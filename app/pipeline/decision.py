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
    MISSING_CONTEXT_KEYWORDS = [
        "unavailable",
        "missing",
        "unknown",
        "not provided",
        "cannot determine",
        "insufficient information",
        "foul count unknown",
        "fatigue index unavailable",
    ]
    FOUL_TROUBLE_KEYWORDS = [
        "5 fouls",
        "five fouls",
        "fouled out",
        "foul trouble",
    ]

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

    # --- Rule 2: Missing critical context -> abstain ---
    if any(word in reason for word in MISSING_CONTEXT_KEYWORDS):
        return {
            "answer": "abstain",
            "model_reason": parsed_output["reason"],
            "reason": "missing_critical_context",
            "confidence": confidence,
            "decision_type": "abstained"
        }

    # --- Rule 3: Foul-out or severe foul trouble -> do_not_extend ---
    if any(word in reason for word in FOUL_TROUBLE_KEYWORDS):
        return {
            "answer": "do_not_extend",
            "model_reason": parsed_output["reason"],
            "reason": "foul_trouble_risk",
            "confidence": confidence,
            "decision_type": "override"
        }

    # --- Rule 4: Low confidence -> abstain ---
    if confidence < ABSTAIN_THRESHOLD:
        return {
            "answer": "abstain",
            "model_reason": parsed_output["reason"],
            "reason": "confidence_below_threshold",
            "confidence": confidence,
            "decision_type": "abstained"
        }

    # --- Rule 5: Respect explicit abstain (do not force override) ---
    if answer == "abstain":
        return {
            "answer": "abstain",
            "model_reason": parsed_output["reason"],
            "reason": "model_selected_abstain",
            "confidence": confidence,
            "decision_type": "abstained"
        }


    # --- Rule 6: Weak/empty reasoning -> abstain ---
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