from app.pipeline.orchestrator import ask_basketball_question


def main():
    question = input("Ask a basketball question: ").strip()

    if not question:
        print("No question entered.")
        return

    mode = input("Structured output? (yes/no): ").strip().lower()
    structured = mode == "yes"

    result = ask_basketball_question(question, structured=structured)

    print("\n--- Response ---")

    if isinstance(result, dict) and "error_type" in result:
        print(f"Error Type: {result['error_type']}")
        print(f"Error Message: {result.get('error_message')}")
        return

    if structured:
        print(f"Answer: {result.get('answer')}")
        print(f"Reason: {result.get('reason')}")
        print(f"Confidence: {result.get('confidence')}")
        print(f"Decision Type: {result.get('decision_type')}")
    else:
        print(result)


if __name__ == "__main__":
    main()
