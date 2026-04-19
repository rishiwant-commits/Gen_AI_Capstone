from backend.rag.vector_store import load_vector_store

db = load_vector_store()


def retrieve_knowledge(query):
    docs = db.similarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in docs])