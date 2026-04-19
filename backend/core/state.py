from typing import TypedDict, Optional, Any


class FarmState(TypedDict):
    input: dict
    processed_input: Optional[Any]
    prediction: Optional[float]
    risk: Optional[str]
    issues: list
    recommendations: list
    contributions: Optional[Any]
    context: Optional[str]
    advisory: Optional[dict]


def create_initial_state(user_input: dict) -> FarmState:
    return {
        "input": user_input,
        "processed_input": None,
        "prediction": None,
        "risk": None,
        "issues": [],
        "recommendations": [],
        "contributions": None,
        "context": None,
        "advisory": None
    }
