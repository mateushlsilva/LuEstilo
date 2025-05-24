from pydantic import BaseModel

class WhatsappBase(BaseModel):
    numero: str
    mensagem: str