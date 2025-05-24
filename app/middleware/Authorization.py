from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.config import settings
from typing import List

class Authorization:
    def __init__(self, nivel_requerido: List[str]):
        self.security = HTTPBearer()
        self.nivel_requerido = nivel_requerido

    def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        token = credentials.credentials
        if not credentials:
            raise HTTPException(
                status_code=401,
                detail="Você não está autenticado.",
            )

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_sub = payload.get("sub")
            user_nivel = payload.get("nivel")
            if user_nivel not in self.nivel_requerido:
                raise HTTPException(status_code=403, detail="Acesso negado")
            return {"sub": user_sub, "nivel": user_nivel}  

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")

        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Token inválido")