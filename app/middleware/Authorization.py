from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.config import settings

class Authorization:
    def __init__(self):
        self.security = HTTPBearer()

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
            return payload  

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")

        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Token inválido")