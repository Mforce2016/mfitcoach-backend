from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from app.services.memory_ai_service import analyze_memory
from app.services.memory_service import update_student_memory
from app.models.chat import ChatRequest
from app.services.firebase_service import db
from app.services.openai_service import chat_with_nutrition_ai

router = APIRouter()

COSTO_CHAT = 1


@router.post("")
def nutrition_chat(
    data: ChatRequest,
):

    # Buscar alumno
    alumno_ref = db.collection("alumnos").document(data.dni)

    alumno_doc = alumno_ref.get()

    if not alumno_doc.exists:

        raise HTTPException(
            status_code=404,
            detail="Alumno no encontrado"
        )

    alumno = alumno_doc.to_dict()

    # Verificar fichas
    fichas = alumno.get("fichas", 0)

    if fichas < COSTO_CHAT:

        raise HTTPException(
            status_code=400,
            detail="Fichas insuficientes"
        )

    # Consumir ficha
    nuevas_fichas = fichas - COSTO_CHAT

    alumno_ref.update({
        "fichas": nuevas_fichas
    })

    # Analizar memoria IA
    memory_data = analyze_memory(
        alumno=alumno,
        message=data.message
    )

    update_student_memory(
        dni=data.dni,
        data=memory_data
    )

    # Generar respuesta IA
    respuesta = chat_with_nutrition_ai(
        alumno,
        data.message
    )

    # Guardar historial
    db.collection("chat_history").add({

        "dni": data.dni,

        "mensaje": data.message,

        "respuesta": respuesta,

        "fichas_gastadas": COSTO_CHAT
    })

    return {

        "success": True,

        "reply": respuesta,

        "fichas_restantes": nuevas_fichas
    }