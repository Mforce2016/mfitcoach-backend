from openai import OpenAI

from app.core.config import settings

from app.services.memory_service import get_student_memory

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def generate_chat_response(
    historial,
    alumno
):

    memoria = get_student_memory(
        alumno.get("dni")
    )

    system_prompt = f"""
Eres el coach nutricional IA premium de FitCoach.

Tu trabajo es ayudar al alumno diariamente.

Debes actuar como:

- nutricionista deportivo
- coach fitness
- especialista en hábitos
- motivador
- seguimiento de progreso

DATOS DEL ALUMNO:

Nombre: {alumno.get("nombre")}
Edad: {alumno.get("edad")}
Peso: {alumno.get("peso")}
Altura: {alumno.get("altura")}
Objetivo: {alumno.get("objetivo")}

MEMORIA IA:

{memoria}

REGLAS:

- responde corto y útil
- sé profesional
- sé cálido
- evita respuestas robóticas
- ayuda realmente al alumno
- recuerda conversaciones anteriores
- da consejos aplicables
- adapta recomendaciones al objetivo
"""

    messages = [

        {
            "role": "system",
            "content": system_prompt
        }
    ]

    messages.extend(historial)

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=messages,

        temperature=0.7,

        max_tokens=700
    )

    return response.choices[0].message.content