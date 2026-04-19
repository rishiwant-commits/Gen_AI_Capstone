from langchain.llms import HuggingFaceHub
from backend.llm.prompt_template import build_prompt
from backend.rag.retriever import retrieve_knowledge


llm = HuggingFaceHub(
    repo_id="google/flan-t5-large",
    model_kwargs={"temperature": 0.3}
)


def generate_advisory(user_input, prediction, risk, issues):
    query = f"{user_input['Crop_Type']} {' '.join(issues)}"

    context = retrieve_knowledge(query)

    prompt = build_prompt(user_input, prediction, risk, issues, context)

    response = llm(prompt)

    return response, context