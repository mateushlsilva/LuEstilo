from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import auth_service
from app.schemas import authSchema
from app.database import Database
from app.models.clientesModel import Cliente
from app.utils.validated import Validadores

service = auth_service.AuthService()
db = Database()

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=authSchema.Token, summary="Registrar um novo usuário",
description="""
Cria um novo usuário com os dados fornecidos.

Retorna um token de autenticação após o cadastro.
""",
responses={
    200: {"description": "Usuário registrado com sucesso"},
    400: {"description": "Dados inválidos ou usuário já existe"},
})
def register(user: authSchema.UserRegister, db: Session = Depends(db.get_db)):
    validar = Validadores()
    senha = validar.senha(user.senha)
    cpf = validar.validar_cpf(user.cpf)
    if db.query(Cliente).filter_by(email=user.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")

   
    if db.query(Cliente).filter_by(cpf=user.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    if senha == False:
        raise HTTPException(status_code=400, detail="A senha tem que ter 8 caracteres, pelo menos um caractere maiúsculo, um minúsculo, um número e um especial!")
    if cpf == False:
        raise HTTPException(status_code=400, detail="O cpf tem que ter 11 números!")
    if validar.validar_cpf(user.telefone) == False:
        raise HTTPException(status_code=400, detail="O Telefone tem que ser um números existente!")
    db_user = service.register_user(db, user)
    token = service.create_token(db_user.id, db_user.nivel)
    return token

@router.post("/login", response_model=authSchema.Token, summary="Login de usuário",
description="""
Autentica um usuário com email e senha.

Retorna um token de acesso e refresh token se as credenciais forem válidas.
""",
responses={
    200: {"description": "Login bem-sucedido"},
    401: {"description": "Credenciais inválidas"},
})
def login(user: authSchema.UserLogin, db: Session = Depends(db.get_db)):
    db_user = service.authenticate_user(db, user)
    if not db_user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = service.create_token(db_user.id, db_user.nivel)
    return token

@router.post("/refresh-token", response_model=authSchema.Token, summary="Renovar o token de acesso",
description="""
Gera um novo token de acesso com base em um refresh token válido.

Use essa rota para manter a sessão do usuário ativa sem exigir novo login.
""",
responses={
    200: {"description": "Token renovado com sucesso"},
    401: {"description": "Token inválido ou expirado"},
})
def refresh_token(token: authSchema.RefreshRequest):
    payload = service.jwt_token.verify_token(token.refresh_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    user_id = payload.get("sub")
    nivel = payload.get("nivel")
    return service.create_token(user_id, nivel)
