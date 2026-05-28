from pydantic import BaseModel


class ChatRequest(BaseModel):

    dni: str
    message: str