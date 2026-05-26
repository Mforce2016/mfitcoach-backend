from pydantic import BaseModel


class NutritionRequest(BaseModel):
    dni: str
    objetivo: str
    peso: float
    altura: float
    edad: int
    restricciones: str = ""