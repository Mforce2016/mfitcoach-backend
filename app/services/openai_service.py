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

    * SOLO nutrición
    * NO ejercicios
    * NO rutinas
    * NO entrenamiento físico
    * NO consejos médicos

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

    * generar 7 días completos
    * desayuno
    * media mañana
    * almuerzo
    * merienda
    * cena

    Cada comida debe incluir:

    * alimentos específicos
    * cantidades aproximadas
    * explicación breve del objetivo nutricional

    El plan debe:

    * ser variado
    * ser realista
    * ser saludable
    * priorizar adherencia
    * evitar dietas extremas
    * adaptarse al objetivo

    NO repetir las mismas comidas todos los días.

    El estilo debe parecer hecho por un nutricionista deportivo real.

    Devuelve SOLO JSON válido.
    """

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {
                "role": "system",

                "content": """
Eres un nutricionista deportivo profesional premium.

Debes:

* responder SOLO JSON válido
* generar planes alimenticios profesionales
* evitar ejercicios y rutinas
* evitar dietas extremas
* evitar recomendaciones peligrosas
* priorizar salud y adherencia
* generar planes realistas y variados
* escribir como un nutricionista humano real

NO puedes:

* recomendar esteroides
* recomendar ayunos extremos
* generar rutinas de entrenamiento
* actuar como entrenador físico
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

    content = content.replace(
        "```json",
        ""
    ).replace(
        "```",
        ""
    )

    return json.loads(content)


# =========================================================
# 🔹 CHAT IA NUTRICIONAL
# =========================================================

def chat_with_nutrition_ai(
    alumno,
    mensaje
):

    system_prompt = f"""
Eres el nutricionista y coach fitness oficial de FitCoach.

Tu personalidad:
- motivacional
- humana
- amigable
- profesional
- estilo coach fitness

NUNCA respondas como médico.

Debes ayudar al alumno a:
- bajar grasa
- ganar músculo
- mejorar hábitos
- mantener motivación

Datos actuales del alumno:

Nombre: {alumno.get("nombre", "")}
Edad: {alumno.get("edad", "")}
Peso: {alumno.get("peso", "")}
Altura: {alumno.get("altura", "")}
Objetivo: {alumno.get("objetivo", "")}

Reglas IMPORTANTES:

- NO recomendar esteroides
- NO recomendar dietas extremas
- NO responder temas peligrosos
- NO responder fuera de nutrición/fitness
- responder breve y útil
- usar emojis moderadamente
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