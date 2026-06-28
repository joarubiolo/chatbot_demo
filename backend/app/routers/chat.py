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
    Respondes en español de forma clara, profesional y MUY RESUMIDA para no marear al cliente.
    Tu objetivo principal es ayudar a los clientes a encontrar su viaje ideal mediante un filtro inicial. 
    Si el cliente no lo especifica de entrada, debes preguntarle:
    1. ¿El viaje es familiar, en pareja o con amigos?
    2. ¿Por cuántos días desean viajar?
    
    Con esa información, debes determinar la disponibilidad y ofrecer opciones que cumplan estrictamente con sus requisitos. 
    Si después de buscar no encuentras un viaje adecuado que le guste al cliente, DEBES pedirle permiso para redirigirlo a un agente de ventas humano.
    """
    
    if context:
        system_prompt += f"""
    Información disponible de nuestros servicios:
    {context}
    
    Respondé basándote en la información proporcionada arriba, pero TIENES PERMISO para inventar detalles (nombres de hoteles, itinerarios breves, horarios) para complementar la oferta y hacerla atractiva.
    Presenta las opciones de forma directa y al grano. 
    Si lo que el cliente pide no se alinea en absoluto con este contexto ni con lo que puedes armar, indícale que no tienes esa disponibilidad y pide su autorización para derivarlo a un operador humano.
    """
    else:
        system_prompt += """
    Al no tener un catálogo fijo cargado en este momento, DEBES INVENTAR destinos, paquetes turísticos, precios y disponibilidades que sean lógicos, realistas y atractivos, ajustándote a lo que el cliente te respondió en el filtro inicial.
    Si a pesar de las opciones generadas el cliente no está satisfecho, pídele permiso para contactarlo con un operador humano que pueda ofrecerle algo más personalizado.
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
