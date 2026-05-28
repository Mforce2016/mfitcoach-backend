from datetime import datetime

from fastapi import APIRouter
from fastapi import HTTPException
from app.models.chat import ChatRequest
from app.services.firebase_service import db
from app.services.memory_ai_service import analyze_memory
from app.services.memory_service import update_student_memory
from app.services.chat_service import generate_chat_response

router = APIRouter()

COSTO_CHAT = 1

@router.post("")
def nutrition_chat(
    data: ChatRequest,
):

    # =====================================================
    # 🔹 BUSCAR ALUMNO
    # =====================================================

    alumno_ref = (
        db.collection("alumnos")
        .document(data.dni)
    )

    alumno_doc = alumno_ref.get()

    if not alumno_doc.exists:

        raise HTTPException(
            status_code=404,
            detail="Alumno no encontrado"
        )

    alumno = alumno_doc.to_dict()

    # =====================================================
    # 🔹 VERIFICAR FICHAS
    # =====================================================

    fichas = alumno.get("fichas", 0)

    if fichas < COSTO_CHAT:

        raise HTTPException(
            status_code=400,
            detail="Fichas insuficientes"
        )

    # =====================================================
    # 🔹 DESCONTAR FICHA
    # =====================================================

    nuevas_fichas = fichas - COSTO_CHAT

    alumno_ref.update({

        "fichas": nuevas_fichas
    })

    # =====================================================
    # 🔹 ANALIZAR MEMORIA IA
    # =====================================================

    try:

        memory_data = analyze_memory(

            alumno=alumno,

            message=data.message
        )

        update_student_memory(

            dni=data.dni,

            data=memory_data
        )

    except Exception as e:

        print("ERROR MEMORIA IA:", e)

    # =====================================================
    # 🔹 OBTENER HISTORIAL CHAT
    # =====================================================

    history_docs = (

        db.collection("chat_history")
        .where("dni", "==", data.dni)
        .order_by("timestamp")
        .limit_to_last(10)
        .get()

    )

    historial = []

    for doc in history_docs:

        item = doc.to_dict()

        historial.append({

            "role": "user",

            "content": item.get(
                "mensaje",
                ""
            )
        })

        historial.append({

            "role": "assistant",

            "content": item.get(
                "respuesta",
                ""
            )
        })

    # =====================================================
    # 🔹 NUEVO MENSAJE USUARIO
    # =====================================================

    historial.append({

        "role": "user",

        "content": data.message
    })

    # =====================================================
    # 🔹 GENERAR RESPUESTA IA
    # =====================================================

    try:

        respuesta = generate_chat_response(

            historial=historial,

            alumno=alumno
        )

    except Exception as e:

        print("ERROR OPENAI:", e)

        respuesta = (
            "⚠️ Rou está tardando más de lo normal. "
            "Intentá nuevamente en unos segundos."
        )

    # =====================================================
    # 🔹 GUARDAR HISTORIAL
    # =====================================================

    db.collection("chat_history").add({

        "dni": data.dni,

        "mensaje": data.message,

        "respuesta": respuesta,

        "fichas_gastadas": COSTO_CHAT,

        "timestamp": datetime.utcnow()
    })

    # =====================================================
    # 🔹 RESPUESTA FINAL
    # =====================================================

    return {

        "success": True,

        "reply": respuesta,

        "fichas_restantes": nuevas_fichas
    }