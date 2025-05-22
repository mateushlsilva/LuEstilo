from sqlalchemy.orm import Session
from app.models.clientesModel import Cliente
from app.schemas.clienteSchema import ClienteRead, ClienteBase
from typing import Optional
from app.utils.auth import Auth

class ClienteService:
    def __init__(self):
        self.auth = Auth()

    def criar_cliente(self, db: Session, cliente: ClienteBase):
        senha = self.auth.hash_senha(cliente.senha)
        novo_cliente = Cliente(
            nome=cliente.nome,
            email=cliente.email,
            cpf=cliente.cpf,
            telefone=cliente.telefone,
            senha=senha  
        )
        db.add(novo_cliente)
        db.commit()
        db.refresh(novo_cliente)
        return novo_cliente

    def pegar_todos_clientes(
        self, 
        db: Session,
        nome: Optional[str],
        email: Optional[str],
        skip: int,
        limit: int
    ):
        query = db.query(Cliente)

        if nome:
            query = query.filter(Cliente.nome.ilike(f"%{nome}%"))
        if email:
            query = query.filter(Cliente.email.ilike(f"%{email}%"))

        
        return query.offset(skip).limit(limit).all()

    def pegar_cliente_id(self, db: Session, id: int):
        return db.query(Cliente).filter(Cliente.id == id).first()

    def alterar_cliente(self, db: Session, id: int, dados: ClienteBase):
        cliente = db.query(Cliente).filter(Cliente.id == id).first()
        if not cliente:
            return None

        if cliente.email != dados.email:
            if db.query(Cliente).filter(Cliente.email == dados.email).first():
                raise ValueError("Email já está em uso.")

        if cliente.cpf != dados.cpf:
            if db.query(Cliente).filter(Cliente.cpf == dados.cpf).first():
                raise ValueError("CPF já está em uso.")

       
        cliente.nome = dados.nome
        cliente.email = dados.email
        cliente.cpf = dados.cpf
        cliente.telefone = dados.telefone
        cliente.senha = self.auth.hash_senha(dados.senha)

        db.commit()
        db.refresh(cliente)
        return cliente


    def deletar_cliente(self, db: Session, id):
        cliente = db.query(Cliente).filter(Cliente.id == id).first()
        if not cliente:
            return None

        db.delete(cliente)
        db.commit()
        return True