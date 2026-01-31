from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

persist_dir = "./rag_store"
collection = "ios_app"
emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vs = Chroma(collection_name=collection, embedding_function=emb, persist_directory=persist_dir)

q = "Generate XCUITest for login invalid password"
docs = vs.similarity_search(q, k=10)

# Build a compact context pack for your LLM:
context_pack = "\n\n".join(
    f"[{d.metadata.get('kind')} | {d.metadata.get('path')} | {d.metadata.get('screen')}]\n{d.page_content}"
    for d in docs
)
print(context_pack[:4000])