from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings


def load_vector_store():
    with open("backend/rag/knowledge_base.txt", "r") as f:
        text = f.read()

    splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    docs = splitter.create_documents([text])

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    db = FAISS.from_documents(docs, embeddings)

    return db