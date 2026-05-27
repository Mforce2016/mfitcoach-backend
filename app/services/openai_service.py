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
Eres un nutricionista deportivo profesional.

Genera un plan alimenticio semanal.

Devuelve SOLO JSON válido.

Datos del alumno:

Objetivo: {data.objetivo}
Peso: {data.peso}
Altura: {data.altura}
Edad: {data.edad}
Sexo: {data.sexo}

Formato:

{{
  "calorias": 0,
  "proteinas": 0,
  "carbohidratos": 0,
  "grasas": 0,

  "lunes": {{
    "desayuno": [],
    "almuerzo": [],
    "merienda": [],
    "cena": []
  }},

  "martes": {{
    "desayuno": [],
    "almuerzo": [],
    "merienda": [],
    "cena": []
  }},

  "miercoles": {{
    "desayuno": [],
    "almuerzo": [],
    "merienda": [],
    "cena": []
  }},

  "jueves": {{
    "desayuno": [],
    "almuerzo": [],
    "merienda": [],
    "cena": []
  }},

  "viernes": {{
    "desayuno": [],
    "almuerzo": [],
    "merienda": [],
    "cena": []
  }},

  "sabado": {{
    "desayuno": [],
    "almuerzo": [],
    "merienda": [],
    "cena": []
  }},

  "domingo": {{
    "desayuno": [],
    "almuerzo": [],
    "merienda": [],
    "cena": []
  }},

  "consejos": []
}}
"""

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {
                "role": "system",

                "content": """
Eres un coach nutricional deportivo premium.

Debes:
- responder SOLO JSON válido
- crear planes saludables
- evitar dietas extremas
- evitar consejos peligrosos
- priorizar salud y rendimiento
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