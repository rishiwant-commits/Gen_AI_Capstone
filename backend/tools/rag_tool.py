from backend.rag.retriever import retrieve_knowledge

def rag_tool(state):
    data = state["input"]
    issues = [i["type"] for i in state["issues"]]

    query = f"""
    Crop: {data['Crop_Type']}
    Issues: {issues}
    Rainfall: {data.get('Rainfall')}
    Soil: {data.get('Soil_Type')}
    """

    context = retrieve_knowledge(query)

    state["context"] = context
    return state