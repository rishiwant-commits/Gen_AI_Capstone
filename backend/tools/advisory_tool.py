import traceback
from backend.llm.advisor import generate_advisory


def advisory_tool(state):
    try:
        advisory = generate_advisory(
            state["input"],
            state["prediction"],
            state["risk"],
            state["issues"],
            state["context"]
        )
    except Exception as e:
        print(f"Advisory tool failed: {traceback.format_exc()}")
        advisory = {
            "summary": "Advisory unavailable due to an internal error.",
            "recommendations": [],
            "risk_explanation": "",
            "actions": []
        }

    state["advisory"] = advisory
    return state
