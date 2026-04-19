def build_prompt(data, prediction, risk, issues, context):
    return f"""
You are an expert agricultural advisor.

Farm Data:
{data}

Predicted Yield: {prediction}
Risk Level: {risk}

Issues:
{issues}

Knowledge:
{context}

Return ONLY valid JSON in this format:

{{
  "summary": "...",
  "recommendations": ["...", "..."],
  "risk_explanation": "...",
  "actions": ["...", "..."]
}}

DO NOT return anything outside JSON.
"""