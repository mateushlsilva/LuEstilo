from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import auth_service
from app.schemas import authSchema
from app.database import Database

service = auth_service.AuthService()
db = Database()

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=authSchema.Token)
def register(user: authSchema.UserRegister, db: Session = Depends(db.get_db)):
    db_user = service.register_user(db, user)
    token = service.create_token(db_user.id)
    return token

@router.post("/login", response_model=authSchema.Token)
def login(user: authSchema.UserLogin, db: Session = Depends(db.get_db)):
    db_user = service.authenticate_user(db, user)
    if not db_user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = service.create_token(db_user.id)
    return token

@router.post("/refresh-token", response_model=authSchema.Token)
def refresh_token(token: str):
    payload = service.jwt_token.verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    user_id = payload.get("sub")
    return service.create_token(user_id)
