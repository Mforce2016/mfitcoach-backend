import json

from openai import OpenAI

from app.core.config import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

# =========================================================
# 🔹 PLAN SEMANAL PREMIUM
# =========================================================

def generate_meal_plan(data):

    prompt = f"""
Eres un nutricionista deportivo profesional de elite.

Debes crear un plan alimenticio semanal COMPLETO y PROFESIONAL.

IMPORTANTE:

- SOLO nutrición
- NO ejercicios
- NO rutinas
- NO entrenamiento físico
- NO consejos médicos

OBJETIVO DEL ALUMNO:
{data.objetivo}

DATOS:

Peso: {data.peso} kg
Altura: {data.altura} cm
Edad: {data.edad}
Sexo: {data.sexo}
Nivel de actividad: {data.nivel_actividad}

Restricciones:
{data.restricciones}

Comidas por día:
{data.comidas_por_dia}

REQUISITOS DEL PLAN:

- generar 7 días completos
- desayuno
- media mañana
- almuerzo
- merienda
- cena

Cada comida debe incluir:

- alimentos específicos
- cantidades aproximadas
- explicación breve del objetivo nutricional

El plan debe:

- ser variado
- ser realista
- ser saludable
- priorizar adherencia
- evitar dietas extremas
- adaptarse al objetivo

NO repetir las mismas comidas todos los días.

El estilo debe parecer hecho por un nutricionista deportivo real.

IMPORTANTE:
RESPONDE SOLO TEXTO PLANO.
NO JSON.
NO MARKDOWN.
"""

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {
                "role": "system",

                "content": """
Eres un nutricionista deportivo profesional premium.

Debes:

- generar planes alimenticios profesionales
- evitar ejercicios y rutinas
- evitar dietas extremas
- evitar recomendaciones peligrosas
- priorizar salud y adherencia
- generar planes realistas y variados
- escribir como un nutricionista humano real

RESPONDE SOLO TEXTO PLANO.

NO JSON.
NO MARKDOWN.
"""
            },

            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.7,

        max_tokens=2500
    )

    content = response.choices[0].message.content

    return {
        "plan": content
    }


# =========================================================
# 🔹 CHAT IA NUTRICIONAL
# =========================================================

def chat_with_nutrition_ai(
    alumno,
    mensaje
):
    system_prompt = f"""
    Eres ROU, el asistente nutricional oficial de FitCoach.

    Tu función es responder consultas rápidas de nutrición,
    alimentación saludable y hábitos.

    IMPORTANTE:

    - NO generar planes alimenticios semanales completos
    - NO generar rutinas de entrenamiento
    - NO crear programas de varios días
    - NO reemplazar al coach humano
    - si el alumno pide un plan semanal, responde que debe usar
      la función premium de "Plan Nutricional"

    Tu estilo:
    - breve
    - profesional
    - humano
    - motivador
    - claro

    Puedes ayudar con:
    - ideas de comidas
    - snacks saludables
    - proteínas
    - calorías
    - hábitos
    - hidratación
    - ansiedad alimentaria
    - organización de comidas
    - dudas nutricionales

    Datos del alumno:

    Nombre: {alumno.get("nombre", "")}
    Edad: {alumno.get("edad", "")}
    Peso: {alumno.get("peso", "")}
    Altura: {alumno.get("altura", "")}
    Objetivo: {alumno.get("objetivo", "")}

    Reglas:
    - responder corto
    - no inventar enfermedades
    - no dar consejos peligrosos
    - no recomendar esteroides
    - no responder temas fuera de nutrición
    """

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": mensaje
            }
        ],

        temperature=0.8,

        max_tokens=400
    )

    return response.choices[0].message.content