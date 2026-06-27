from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
_modelo = None


def get_model():
    global _modelo
    if _modelo is None:
        _modelo = SentenceTransformer(MODEL_NAME)
    return _modelo


def generar_embedding(texto: str) -> list[float]:
    modelo = get_model()
    return modelo.encode(texto).tolist()
