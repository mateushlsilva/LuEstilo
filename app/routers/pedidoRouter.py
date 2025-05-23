from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import Database
from app.services.pedidoService import PedidoService
from app.schemas.pedidoSchema import PedidoBase, PedidoRead, PedidoCreate, PedidoRemove, PedidoStatus

router = APIRouter(prefix="/orders", tags=["Pedidos"])
service = PedidoService()
db = Database()

@router.post("/", response_model=PedidoRead)
def criar_pedido(pedidos: PedidoCreate, db: Session = Depends(db.get_db)):
    novo_pedido = service.criar_pedido(db, pedidos)
    return novo_pedido


@router.get("/", response_model=List[PedidoRead])
def listar_pedidos(
    periodo: Optional[str] = Query(None),
    secao_produtos: Optional[str] = Query(None),
    id_pedido: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    cliente: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(db.get_db)
):
    return service.pegar_todos_pedidos(db, periodo, secao_produtos, id_pedido, status, cliente, skip, limit)

@router.get("/{id}", response_model=PedidoRead)
def buscar_pedidos(id: int, db: Session = Depends(db.get_db)):
    pedidos = service.pegar_pedidos_id(db, id)
    if not pedidos:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedidos

@router.delete("/{id}",  response_model=PedidoRemove)
def deletar_pedido(id: int, db: Session = Depends(db.get_db)):
    pedido = service.deletar_pedido(db, id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"detail": 'Pedido deletado!'}


@router.put("/{id}", response_model=PedidoRead)
def atualizar_pedido(id: int, pedido: PedidoCreate, db: Session = Depends(db.get_db)):
    try:
        pedido_atualizado = service.alterar_pedido(db, id, pedido)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not pedido_atualizado:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    return pedido_atualizado


@router.patch("/{id}", response_model=PedidoRead)
def atualizar_status(id: int, status: PedidoStatus, db: Session = Depends(db.get_db)):
    pedido = service.patch_status_pedido(db, id, status)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido