from passlib.context import CryptContext

class Auth():
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_senha(self, senha: str) -> str:
        return self.pwd_context.hash(senha)

    def verificar_senha(self, senha_plain: str, senha_hash: str) -> bool:
        return self.pwd_context.verify(senha_plain, senha_hash)
