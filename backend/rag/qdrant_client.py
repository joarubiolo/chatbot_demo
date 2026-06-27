from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config import settings

client = QdrantClient(path=settings.qdrant_path)

COLLECTION_NAME = "turismo"
VECTOR_SIZE = 384


def ensure_collection():
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION_NAME not in names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )


ensure_collection()
