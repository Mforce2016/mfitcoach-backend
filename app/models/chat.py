from pydantic import BaseModel


class ChatRequest(BaseModel):

    dni: str

    mensaje: str