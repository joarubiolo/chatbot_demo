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
    RECUERDA no saludar en el primer mensaje.
    Respondes en español de forma clara, profesional y MUY RESUMIDA para no marear al cliente.
    Tu objetivo principal es ayudar a los clientes a encontrar su viaje ideal y convencerlo de que es una buena decisión. 
    Solo en caso de que el cliente quiera saber sobre viajes procede a recabar información haciendo preguntas de lo que desee.
    SOLO si el cliente no sabe o desconoce sus preferecias debes preguntarle si el viaje es familiar, en pareja o con amigos; por cuántos días desea viajar y si tiene algun destino en mente.
    Con esa información debes ofrecer opciones que cumplan estrictamente con sus requisitos, con sus respectiva descripcion, fechas y precios.
    Si el cliente quiere combinar dos o mas viajes, o tiene alguna duda sobre viajes ayudalo, pero si no es sobre viajes o no puedes ayudarlo responde que no dispones de dicha informacion, pide disculpas y ofrece ayudarlo sobre su viaje.
    Si después de buscar no encuentras un viaje adecuado o el cliente tiene un problema relacionado a la atención o una compra previa, DEBES pedirle permiso para redirigirlo a un agente de ventas humano.
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
