from dataclasses import dataclass


@dataclass
class VectorDocument:
    id: str
    text: str
    metadata: dict


class VectorStore:
    async def upsert(self, documents: list[VectorDocument]) -> None:
        raise NotImplementedError

    async def search(self, query: str, limit: int = 5) -> list[VectorDocument]:
        raise NotImplementedError


class InMemoryVectorStore(VectorStore):
    def __init__(self):
        self.documents: dict[str, VectorDocument] = {}

    async def upsert(self, documents: list[VectorDocument]) -> None:
        for document in documents:
            self.documents[document.id] = document

    async def search(self, query: str, limit: int = 5) -> list[VectorDocument]:
        query_terms = set(query.lower().split())
        scored = []
        for document in self.documents.values():
            overlap = len(query_terms.intersection(document.text.lower().split()))
            scored.append((overlap, document))
        return [document for _, document in sorted(scored, key=lambda item: item[0], reverse=True)[:limit]]


def get_vector_store() -> VectorStore:
    # Replace with Pinecone or Weaviate implementation when credentials are configured.
    return InMemoryVectorStore()
