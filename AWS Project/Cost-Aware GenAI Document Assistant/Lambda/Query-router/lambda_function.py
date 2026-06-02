import json

SIMPLE_KEYWORDS = [
    "what",
    "define",
    "who",
    "when"
]

COMPLEX_KEYWORDS = [
    "compare",
    "analyze",
    "why",
    "architecture",
    "trade-off"
]


def classify_question(question):
    question_lower = question.lower()

    # Complex question detection
    for keyword in COMPLEX_KEYWORDS:
        if keyword in question_lower:
            return "complex"

    # Simple question detection
    for keyword in SIMPLE_KEYWORDS:
        if keyword in question_lower:
            return "simple"

    # Length-based fallback
    if len(question.split()) > 15:
        return "complex"

    return "simple"


def lambda_handler(event, context):

    question = event.get("question", "")

    question_type = classify_question(question)

    if question_type == "simple":
        model = "amazon.titan-text-lite-v1"
        estimated_cost = 0.0002
    else:
        model = "anthropic.claude-3-haiku"
        estimated_cost = 0.0025

    response = {
        "question": question,
        "question_type": question_type,
        "selected_model": model,
        "estimated_cost_usd": estimated_cost
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }