from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore

embedding_service = EmbeddingService()
vector_store = VectorStore()

def retrieve_context(query: str, chat_id: str):
    query_embedding = embedding_service.embed_query(query)
    results = vector_store.similarity_search(query_embedding, chat_id)

    docs = results.get("documents", [[]])[0]
    return "\n\n".join(docs)
