"""
Carga vectores desde vectors.json a Qdrant al iniciar el servidor.
Esto asegura persistencia en Render (disco efímero) restaurando
los datos desde el archivo commiteado en el repo.
"""

import json
import logging
from pathlib import Path

from qdrant_client.models import PointStruct

from rag.qdrant_client import get_client, COLLECTION_NAME, get_vector_size

logger = logging.getLogger(__name__)
VECTORS_FILE = Path(__file__).resolve().parent / "vectors.json"


def seed_from_file():
    if not VECTORS_FILE.exists():
        logger.info("No se encontró vectors.json, se omite seed")
        return

    try:
        data = json.loads(VECTORS_FILE.read_text())
    except (json.JSONDecodeError, Exception) as e:
        logger.warning(f"Error leyendo vectors.json: {e}")
        return

    if not data:
        logger.info("vectors.json está vacío, se omite seed")
        return

    client = get_client()

    # Verificar si ya hay datos en Qdrant
    existing = client.count(collection_name=COLLECTION_NAME)
    if existing.count > 0:
        logger.info(f"Qdrant ya tiene {existing.count} vectores, se omite seed")
        return

    points = []
    for item in data:
        vec = item.get("vector", [])
        if len(vec) != get_vector_size():
            logger.warning(
                f"Vector con dimensión {len(vec)} != esperado {get_vector_size()}, se omite"
            )
            continue
        points.append(
            PointStruct(
                id=item["id"],
                vector=vec,
                payload=item.get("payload", {}),
            )
        )

    if points:
        client.upsert(collection_name=COLLECTION_NAME, points=points)
        logger.info(f"Seed completado: {len(points)} vectores cargados desde vectors.json")
