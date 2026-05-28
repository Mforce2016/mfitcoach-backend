import json

from openai import OpenAI

from app.core.config import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def analyze_memory(
    alumno,
    message
):

    prompt = f"""
Analiza el mensaje del alumno.

Extrae SOLO datos importantes permanentes.

Alumno:

{alumno}

Mensaje:

{message}

Devuelve SOLO JSON.

Formato:

{{
  "objetivo": "",
  "restricciones": [],
  "habitos": [],
  "alimentos_favoritos": [],
  "alimentos_no_gustan": [],
  "suplementos": [],
  "motivacion": ""
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

        temperature=0.2,

        max_tokens=300
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