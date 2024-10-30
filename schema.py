from pydantic import BaseModel

class ChatRequest(BaseModel):
    id: str
    dict_of_vars: dict
    prompt: str
    testResults : optional[dict] = None
