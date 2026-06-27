from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config import settings

COLLECTION_NAME = "turismo"
VECTOR_SIZE = 384

_client = None


def get_client():
    global _client
    if _client is None:
        _client = QdrantClient(path=settings.qdrant_path)
        _ensure_collection()
    return _client


def _ensure_collection():
    collections = _client.get_collections().collections
    names = [c.name for c in collections]
    if COLLECTION_NAME not in names:
        _client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
