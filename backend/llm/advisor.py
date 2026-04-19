from langchain_huggingface import HuggingFaceEndpoint
from backend.llm.prompt_template import build_prompt
from backend.rag.retriever import retrieve_knowledge
import os
import json
import traceback
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-large",
    temperature=0.3,
    huggingfacehub_api_token=os.environ.get("HUGGINGFACEHUB_API_TOKEN", "")
)


def generate_advisory(user_input, prediction, risk, issues, context):
    prompt = build_prompt(user_input, prediction, risk, issues, context)

    try:
        response = llm(prompt)

        # Try to parse JSON
        parsed = json.loads(response)
        return parsed

    except json.JSONDecodeError:
        # LLM returned free text — wrap it gracefully
        return {
            "summary": response if isinstance(response, str) else "Advisory generated.",
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
