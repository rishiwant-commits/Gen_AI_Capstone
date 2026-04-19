def build_prompt(data, prediction, risk, issues, context):
    return f"""
You are an agricultural expert AI.

Farm Data:
{data}

Predicted Yield: {prediction}
Risk Level: {risk}

Detected Issues:
{issues}

Relevant Agricultural Knowledge:
{context}

Task:
Generate a structured advisory report:

1. Crop Summary
2. Yield Analysis
3. Risk Explanation
4. Key Issues
5. Recommendations (actionable)
6. Sources
7. Disclaimer

Be precise and avoid generic advice.
"""