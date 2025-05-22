from pydantic import BaseModel, EmailStr


class ClienteBase(BaseModel):
    email: EmailStr
    cpf: str
    telefone: str
    nome: str
    senha: str

class ClienteRead(ClienteBase):
    id: int

    class Config:
        orm_mode = True
