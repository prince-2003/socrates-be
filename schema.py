from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str
    dict_of_vars: dict