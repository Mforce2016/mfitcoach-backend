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
    Eres ROU, el asistente nutricional premium de Coach Routine.

    Tu función es ayudar al alumno EXCLUSIVAMENTE en temas de:

    * nutrición
    * alimentación saludable
    * hábitos
    * hidratación
    * suplementación básica segura
    * motivación
    * organización alimenticia

    NO eres entrenador físico.

    PROHIBIDO:

    * crear rutinas de gimnasio
    * recomendar ejercicios
    * crear entrenamientos
    * actuar como preparador físico
    * responder temas médicos

    Si el alumno pide ejercicios o rutinas,
    indica que debe consultarlo con su coach.

    DATOS DEL ALUMNO:

    Nombre: {alumno.get("nombre")}
    Edad: {alumno.get("edad")}
    Peso: {alumno.get("peso")}
    Altura: {alumno.get("altura")}
    Objetivo: {alumno.get("objetivo")}

    MEMORIA IA:

    {memoria}

    REGLAS:

    * responde breve y útil
    * sé humano y profesional
    * evita respuestas robóticas
    * adapta consejos al objetivo
    * recuerda conversaciones previas
    * prioriza hábitos sostenibles
    * usa emojis solo ocasionalmente
    * no inventes datos
    * no des consejos peligrosos

    MUY IMPORTANTE:

    Si el alumno pide:

    * plan semanal
    * dieta completa
    * menú de 7 días
    * plan alimenticio completo

    NO lo generes.

    Indícale que debe usar la función premium de plan nutricional semanal.
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