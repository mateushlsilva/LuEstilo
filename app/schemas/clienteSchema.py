from pydantic import BaseModel, EmailStr


class ClienteBase(BaseModel):
    email: EmailStr
    cpf: str
    telefone: str
    nome: str
    senha: str
    nivel: str

class ClienteRemove(BaseModel):
    detail: str
class ClienteRead(ClienteBase):
    id: int

    class Config:
        orm_mode = True
