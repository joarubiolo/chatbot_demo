from openai import OpenAI

from app.config import settings

_clients: dict[str, OpenAI] = {}


def _get_openai() -> OpenAI:
    if "embeddings" not in _clients:
        _clients["embeddings"] = OpenAI(
            base_url=settings.openrouter_base_url,
            api_key=settings.openrouter_api_key,
        )
    return _clients["embeddings"]


def generar_embedding(texto: str) -> list[float]:
    try:
        client = _get_openai()
        response = client.embeddings.create(
            model=settings.embedding_model,
            input=texto,
        )
        return response.data[0].embedding
    except Exception:
        return []
