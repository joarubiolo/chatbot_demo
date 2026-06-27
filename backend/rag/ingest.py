"""
Script de ingesta de documentos PDF a Qdrant.

Uso:
    python -m rag.ingest

Busca archivos .pdf en documents/ y los indexa en la colección "turismo".
"""

from pathlib import Path
from qdrant_client.models import PointStruct

from rag.embeddings import generar_embedding
from rag.qdrant_client import client, COLLECTION_NAME

DOCUMENTS_DIR = Path(__file__).resolve().parent.parent / "documents"


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Divide un texto en chunks de tamaño fijo con solapamiento."""
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
    """Extrae texto de un archivo PDF usando pypdf."""
    from pypdf import PdfReader

    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def ingest_all():
    pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))
    if not pdf_files:
        print("No se encontraron archivos PDF en documents/")
        return

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
            vector = generar_embedding(chunk)
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
        print(f"  -> {len(points)} chunks indexados")


if __name__ == "__main__":
    ingest_all()
