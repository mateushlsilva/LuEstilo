from sqlalchemy.orm import Session
from app.utils import jwt, auth
from app.models import clientesModel  
from app.schemas.authSchema import UserLogin, UserRegister

class AuthService():
    def __init__(self):
        self.authenticate = auth.Auth()
        self.jwt_token = jwt.Jwt()


    def register_user(self, db: Session, user: UserRegister):
        hashed_password = self.authenticate.hash_senha(user.senha)
        db_user = clientesModel(nome=user.nome, email=user.email, senha=hashed_password, cpf=user.cpf, telefone=user.telefone)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def authenticate_user(self, db: Session, user: UserLogin):
        db_user = db.query(clientesModel).filter(clientesModel.email == user.email).first()
        if not db_user or not self.authenticate.verificar_senha(user.senha, db_user.senha):
            return None
        return db_user

    def create_token(self, user_id: int):
        return self.jwt_token.create_access_token(data={"sub": str(user_id)})
