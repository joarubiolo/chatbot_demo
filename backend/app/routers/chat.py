from fastapi import APIRouter, HTTPException
from openai import OpenAI

from app.config import settings
from app.models.schemas import ChatRequest, ChatResponse
from rag.search import buscar_contexto

router = APIRouter()

client = OpenAI(
    base_url=settings.openrouter_base_url,
    api_key=settings.openrouter_api_key,
)


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    context = buscar_contexto(request.message)

    system_prompt = f"""
Eres el asistente virtual de una agencia de viajes.
Respondes en español de forma clara y profesional.
Ayudas a los clientes con información sobre destinos, paquetes turísticos, precios y disponibilidad.
"""
    if context:
        system_prompt += f"""
Información disponible de nuestros servicios:
{context}

Respondé basándote exclusivamente en la información proporcionada arriba.
Si la pregunta del cliente no tiene relación con la información disponible, indicá que no tenés esa información y sugerí contactar a un operador humano.
"""
    else:
        system_prompt += """
Si no tienes información disponible sobre lo que te preguntan,
sugiere al cliente contactar a un operador humano para obtener más información.
No inventes precios ni destinos que no estén en tu base de conocimiento.
"""

    try:
        respuesta = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": request.message},
            ],
            max_tokens=settings.max_tokens,
        )
        content = respuesta.choices[0].message.content or ""
        return ChatResponse(response=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del LLM: {str(e)}")
