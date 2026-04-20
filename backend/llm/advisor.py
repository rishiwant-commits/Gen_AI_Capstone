import json
import os
import traceback
from functools import lru_cache

from backend.llm.prompt_template import build_prompt
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


def _get_groq_api_key() -> str:
    """
    Streamlit Cloud does not load local `.env` files by default.
    Prefer environment variables, then fall back to Streamlit Secrets if available.
    """
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key

    try:
        import streamlit as st  # optional dependency at runtime

        key = st.secrets.get("GROQ_API_KEY")
        if key:
            return str(key)
    except Exception:
        # Don't fail import-time if Streamlit isn't available or secrets missing.
        pass

    return ""


@lru_cache(maxsize=1)
def _get_llm() -> ChatGroq:
    """
    Lazily construct the LLM so missing keys don't crash the app at import time.
    """
    api_key = _get_groq_api_key()
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not set. Set it as an environment variable or in Streamlit Secrets."
        )

    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        groq_api_key=api_key,
    )


def generate_advisory(user_input, prediction, risk, issues, context):
    prompt = build_prompt(user_input, prediction, risk, issues, context)

    try:
        llm = _get_llm()
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
