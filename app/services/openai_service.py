import os
import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_meal_plan(data):

    prompt = f"""
    Actúa como un nutricionista deportivo profesional.

    Genera un plan alimenticio en formato JSON.

    Datos del alumno:

    Objetivo: {data.objetivo}
    Peso: {data.peso} kg
    Altura: {data.altura} cm
    Edad: {data.edad}
    Restricciones: {data.restricciones}

    Devuelve:

    {{
      "calorias": number,
      "proteinas": number,
      "carbohidratos": number,
      "grasas": number,
      "desayuno": [],
      "almuerzo": [],
      "merienda": [],
      "cena": []
    }}
    """

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.7
    )

    content = response.choices[0].message.content

    return json.loads(content)