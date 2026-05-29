from fastapi import APIRouter
from fastapi import HTTPException

from app.models.nutrition import NutritionRequest

from app.services.firebase_service import db
from app.services.openai_service import generate_meal_plan

router = APIRouter()

COSTO_PLAN = 20


@router.post("/generate-meal-plan")
def generate_plan(
    data: NutritionRequest
):

    alumno_ref = db.collection("alumnos").document(data.dni)

    alumno_doc = alumno_ref.get()

    if not alumno_doc.exists:

        raise HTTPException(
            status_code=404,
            detail="Alumno no encontrado"
        )

    alumno = alumno_doc.to_dict()

    fichas = alumno.get("fichas", 0)

    if fichas < COSTO_PLAN:

        raise HTTPException(
            status_code=400,
            detail="Fichas insuficientes"
        )

    nuevas_fichas = fichas - COSTO_PLAN

    alumno_ref.update({
        "fichas": nuevas_fichas
    })

    plan = generate_meal_plan(data)

    db.collection("meal_plans").add({

        "dni": data.dni,

        "objetivo": data.objetivo,

        "plan": plan,

        "fichas_gastadas": COSTO_PLAN
    })

    return {

        "success": True,

        "fichas_restantes": nuevas_fichas,

        "plan": plan["plan"]
    }