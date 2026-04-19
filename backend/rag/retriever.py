from backend.rag.vector_store import load_vector_store
from functools import lru_cache

# Load DB once (important)
db = load_vector_store()


@lru_cache(maxsize=50)
def retrieve_knowledge(query: str) -> str:
    """
    Retrieve top relevant knowledge chunks using similarity search.
    Cached to avoid repeated FAISS calls.
    """

    if not query or query.strip() == "":
        return ""

    docs = db.similarity_search(query, k=3)

    if not docs:
        return ""

    return "\n".join([doc.page_content for doc in docs])