from langchain_groq import ChatGroq
from backend.llm.prompt_template import build_prompt
import os
import json
import traceback
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    groq_api_key=os.environ.get("GROQ_API_KEY", "")
)


def generate_advisory(user_input, prediction, risk, issues, context):
    prompt = build_prompt(user_input, prediction, risk, issues, context)

    try:
        # ChatGroq requires invoke() with messages format
        response = llm.invoke([{"role": "user", "content": prompt}])
        
        # Extract content from response
        response_text = response.content if hasattr(response, 'content') else str(response)

        # Try to parse JSON
        parsed = json.loads(response_text)
        return parsed

    except json.JSONDecodeError:
        # LLM returned free text — wrap it gracefully
        return {
            "summary": response_text if isinstance(response_text, str) else "Advisory generated.",
            "recommendations": [],
            "risk_explanation": f"Risk level: {risk}",
            "actions": []
        }

    except Exception as e:
        print(f"LLM ERROR: {traceback.format_exc()}")
        return {
            "summary": "Advisory could not be generated due to a service error.",
            "recommendations": [],
            "risk_explanation": "",
            "actions": []
        }
