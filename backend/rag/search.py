from rag.embeddings import generar_embedding
from rag.qdrant_client import get_client, COLLECTION_NAME


def buscar_contexto(pregunta: str, limite: int = 3) -> str:
    try:
        client = get_client()
        vector = generar_embedding(pregunta)
        resultados = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=limite,
        )

        if not resultados:
            return ""

        contexto_parts = []
        for r in resultados:
            texto = r.payload.get("texto", "")
            archivo = r.payload.get("archivo", "")
            if texto:
                contexto_parts.append(f"[{archivo}] {texto}")

        return "\n\n".join(contexto_parts)
    except Exception:
        return ""
