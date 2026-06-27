"""
Script de ingesta de documentos PDF a Qdrant.

Uso:
    python -m rag.ingest

Busca archivos .pdf en documents/, genera embeddings vía OpenRouter API,
los indexa en Qdrant y exporta un archivo vectors.json para persistencia.
"""

import json
from pathlib import Path

from qdrant_client.models import PointStruct
from openai import OpenAI

from app.config import settings
from rag.qdrant_client import get_client, COLLECTION_NAME

DOCUMENTS_DIR = Path(__file__).resolve().parent.parent / "documents"
VECTORS_FILE = Path(__file__).resolve().parent / "vectors.json"

_openai_client = OpenAI(
    base_url=settings.openrouter_base_url,
    api_key=settings.openrouter_api_key,
)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            end = text.rfind(" ", 0, end) or end
        chunks.append(text[start:end].strip())
        start = end - overlap
    return [c for c in chunks if c]


def extract_text_from_pdf(path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def generar_embedding_api(texto: str) -> list[float]:
    response = _openai_client.embeddings.create(
        model=settings.embedding_model,
        input=texto,
    )
    return response.data[0].embedding


def ingest_all():
    pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))
    if not pdf_files:
        print("No se encontraron archivos PDF en documents/")
        return

    client = get_client()
    all_points = []

    for pdf_path in pdf_files:
        print(f"Procesando: {pdf_path.name}")
        text = extract_text_from_pdf(pdf_path)

        if not text.strip():
            print(f"  -> Sin texto extraíble, se omite")
            continue

        chunks = chunk_text(text)
        print(f"  -> {len(chunks)} chunks generados")

        points = []
        for i, chunk in enumerate(chunks):
            print(f"  -> Generando embedding para chunk {i+1}/{len(chunks)}")
            vector = generar_embedding_api(chunk)
            points.append(
                PointStruct(
                    id=f"{pdf_path.stem}-{i}",
                    vector=vector,
                    payload={
                        "texto": chunk,
                        "archivo": pdf_path.name,
                        "chunk": i,
                    },
                )
            )

        client.upsert(collection_name=COLLECTION_NAME, points=points)
        print(f"  -> {len(points)} chunks indexados en Qdrant")
        all_points.extend(points)

    # Exportar a vectors.json para persistencia
    export_data = []
    for p in all_points:
        export_data.append({
            "id": p.id,
            "vector": p.vector,
            "payload": p.payload,
        })

    VECTORS_FILE.write_text(json.dumps(export_data, ensure_ascii=False, indent=2))
    print(f"  -> {len(export_data)} vectores exportados a {VECTORS_FILE.name}")


if __name__ == "__main__":
    ingest_all()
