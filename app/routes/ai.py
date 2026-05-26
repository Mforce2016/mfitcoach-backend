from fastapi import APIRouter

from app.models.nutrition import NutritionRequest
from app.services.openai_service import generate_meal_plan
from app.services.firebase_service import db

router = APIRouter()


@router.post("/generate-meal-plan")
def generate_plan(data: NutritionRequest):

    plan = generate_meal_plan(data)

    db.collection("meal_plans").add({

        "dni": data.dni,

        "objetivo": data.objetivo,

        "plan": plan
    })

    return {
        "success": True,
        "plan": plan
    }