from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import Database
from app.services.pedidoService import PedidoService
from app.schemas.pedidoSchema import PedidoBase, PedidoRead, PedidoCreate

router = APIRouter(prefix="/orders", tags=["Pedidos"])
service = PedidoService()
db = Database()

@router.post("/", response_model=PedidoRead)
def criar_pedido(pedidos: PedidoCreate, db: Session = Depends(db.get_db)):
    novo_pedido = service.criar_pedido(db, pedidos)
    return novo_pedido
