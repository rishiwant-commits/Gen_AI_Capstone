import json

def generate_advisory(user_input, prediction, risk, issues):
    query = f"{user_input['Crop_Type']} {issues}"

    context = retrieve_knowledge(query)
    prompt = build_prompt(user_input, prediction, risk, issues, context)

    try:
        response = llm(prompt)

        # 🔥 parse JSON safely
        parsed = json.loads(response)

        return parsed, context

    except Exception as e:
        print("LLM ERROR:", str(e))

        return {
            "summary": "Advisory could not be generated.",
            "recommendations": [],
            "risk_explanation": "",
            "actions": []
        }, context