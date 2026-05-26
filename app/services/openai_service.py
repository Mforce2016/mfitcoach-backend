import json

from openai import OpenAI
from app.core.config import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def generate_meal_plan(data):

    prompt = f"""
Eres un nutricionista deportivo profesional.

Devuelve SOLO JSON válido.

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
  "desayuno": [],
  "almuerzo": [],
  "merienda": [],
  "cena": [],
  "consejos": []
}}
"""

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[
            {
                "role": "system",
                "content": "Responde SOLO JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.7,

        max_tokens=1200
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