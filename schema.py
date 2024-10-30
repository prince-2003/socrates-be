from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    id: str
    dict_of_vars: dict
    prompt: str
    testResults : Optional[dict] = None
