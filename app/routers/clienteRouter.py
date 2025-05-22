from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import Database
from app.schemas.clienteSchema import ClienteBase, ClienteRead, ClienteRemove
from app.services.clienteService import ClienteService
from app.models.clientesModel import Cliente
from app.utils.validated import Validadores

router = APIRouter(prefix="/clients", tags=["Clientes"])
service = ClienteService()
db = Database()


@router.get("/", response_model=List[ClienteRead])
def listar_clientes(
    nome: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(db.get_db)
):
    return service.pegar_todos_clientes(db, nome, email, skip, limit)

@router.get("/{id}", response_model=ClienteRead)
def buscar_cliente(id: int, db: Session = Depends(db.get_db)):
    cliente = service.pegar_cliente_id(db, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.post("/", response_model=ClienteRead)
def criar_cliente(cliente: ClienteBase, db: Session = Depends(db.get_db)):
    validar = Validadores()
    senha = validar.senha(cliente.senha)
    cpf = validar.validar_cpf(cliente.cpf)
    if db.query(Cliente).filter_by(email=cliente.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")

   
    if db.query(Cliente).filter_by(cpf=cliente.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    if senha == False:
        raise HTTPException(status_code=400, detail="A senha tem que ter 8 caracteres, pelo menos um caractere maiúsculo, um minúsculo, um número e um especial!")
    if cpf == False:
        raise HTTPException(status_code=400, detail="O cpf tem que ter 11 números!")
    if validar.validar_cpf(cliente.telefone) == False:
        raise HTTPException(status_code=400, detail="O Telefone tem que ser um números existente!")

    novo_cliente = service.criar_cliente(db, cliente)
    return novo_cliente

@router.delete("/{id}",  response_model=ClienteRemove)
def deletar_cliente(id: int, db: Session = Depends(db.get_db)):
    cliente = service.deletar_cliente(db, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"detail": 'Cliente deletado!'}


@router.put("/{id}", response_model=ClienteRead)
def atualizar_cliente(id: int, cliente: ClienteBase, db: Session = Depends(db.get_db)):
    validar = Validadores()
    try:
        if validar.senha(cliente.senha) == False:
            raise HTTPException(status_code=400, detail="A senha tem que ter 8 caracteres, pelo menos um caractere maiúsculo, um minúsculo, um número e um especial!")
        if validar.validar_cpf(cliente.cpf) == False:
            raise HTTPException(status_code=400, detail="O cpf tem que ter 11 números!")
        if validar.validar_cpf(cliente.telefone) == False:
            raise HTTPException(status_code=400, detail="O Telefone tem que ser um números existente!")
        
        cliente_atualizado = service.alterar_cliente(db, id, cliente)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not cliente_atualizado:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return cliente_atualizado