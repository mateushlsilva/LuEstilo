from pydantic import BaseModel
from app.schemas.clienteSchema import ClienteBase

class UserRegister(ClienteBase):
    nome: str
    email: str
    senha: str
    cpf: str
    telefone: str

class UserLogin(BaseModel):
    email: str
    senha: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str