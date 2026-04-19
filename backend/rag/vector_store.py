import os
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

DB_PATH = "faiss_index"


def load_vector_store():

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # ✅ LOAD if exists
    if os.path.exists(DB_PATH):
        return FAISS.load_local(
            DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

    # ❗ CREATE only once
    with open("backend/rag/knowledge_base.txt", "r") as f:
        text = f.read()

    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    docs = splitter.create_documents([text])

    db = FAISS.from_documents(docs, embeddings)

    db.save_local(DB_PATH)

    return db