import chromadb

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )
        self.collection = self.client.get_or_create_collection(
            name="pdf_chunks"
        )

    def add_documents(self, embeddings, documents, metadatas, ids):
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print("ChromaDB persisted with", len(ids), "vectors")

    def similarity_search(self, query_embedding, chat_id, k=5):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where={"chat_id": chat_id}
        )
