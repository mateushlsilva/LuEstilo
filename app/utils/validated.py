import re
import string


class Validadores:
    def __init__(self):
        pass

    def senha(self, senha):
        if len(senha) < 8: return False
        tem_maiuscula = any(c.isupper() for c in senha)
        tem_minuscula = any(c.islower() for c in senha)  
        tem_numero    = any(c.isdigit() for c in senha) 
        tem_especial  = any(c in string.punctuation for c in senha)
        print(tem_maiuscula , tem_minuscula , tem_numero , tem_especial)
        return tem_maiuscula and tem_minuscula and tem_numero and tem_especial
    def validar_cpf(self, cpf: str) -> bool:
        return cpf.isdigit() and len(cpf) == 11