from pydantic import BaseModel
from typing import List


class NutritionRequest(BaseModel):

    dni: str
    objetivo: str
    peso: float
    altura: float
    edad: int
    sexo: str
    nivel_actividad: str
    restricciones: List[str] = []
    comidas_por_dia: int = 4