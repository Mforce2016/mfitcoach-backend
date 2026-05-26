from pydantic import BaseModel
from typing import Optional


class ApiResponse(BaseModel):

    success: bool

    message: str

    data: Optional[dict] = None