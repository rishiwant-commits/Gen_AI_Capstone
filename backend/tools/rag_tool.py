from backend.rag.retriever import retrieve_knowledge


def rag_tool(state):
    data = state["input"]
    issue_types = [i["type"] for i in state["issues"]]

    query = (
        f"Crop: {data['Crop_Type']}. "
        f"Issues: {', '.join(issue_types)}. "
        f"Rainfall: {data.get('Rainfall')} mm. "
        f"Soil type: {data.get('Soil_Type')}. "
        f"Season: {data.get('Season')}."
    )

    context = retrieve_knowledge(query)
    state["context"] = context
    return state
