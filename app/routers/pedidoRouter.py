from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import Database
from app.services.pedidoService import PedidoService
from app.schemas.pedidoSchema import PedidoBase, PedidoRead, PedidoCreate, PedidoRemove, PedidoStatus
from app.middleware.Authorization import Authorization


router = APIRouter(prefix="/orders", tags=["Pedidos"], dependencies=[Depends(Authorization(["comum", 'adm']))])
service = PedidoService()
db = Database()

@router.post("/", response_model=PedidoRead,summary="Criar novo pedido",
description="Cria um novo pedido com base nas informações enviadas. Disponível para usuários comuns e administradores.",
responses={
    200: {"description": "Pedido criado com sucesso"},
    400: {"description": "Dados inválidos"},
    403: {"description": "Acesso negado"},
    409: {"description": "Estoque insuficiente"},
})
def criar_pedido(pedidos: PedidoCreate, db: Session = Depends(db.get_db)):
    novo_pedido = service.criar_pedido(db, pedidos)
    return novo_pedido


@router.get("/", response_model=List[PedidoRead], summary="Listar pedidos",
description="Retorna uma lista de pedidos com filtros opcionais como período, seção de produtos, ID, status ou cliente.",
responses={
    200: {"description": "Lista de pedidos retornada com sucesso"},
    403: {"description": "Acesso negado"},
})
def listar_pedidos(
    periodo: Optional[str] = Query(None),
    secao_produtos: Optional[str] = Query(None),
    id_pedido: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    cliente: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 10,
    user=Depends(Authorization(['comum', 'adm'])),
    db: Session = Depends(db.get_db)
):
    cliente_id = None
    if user["nivel"] != "adm":
        cliente_id = int(user["sub"])
    return service.pegar_todos_pedidos(db, periodo, secao_produtos, id_pedido, status, cliente, cliente_id, skip, limit)

@router.get("/{id}", response_model=PedidoRead, summary="Buscar pedido por ID",
description="Busca um pedido específico pelo seu ID.",
responses={
    200: {"description": "Pedido encontrado"},
    404: {"description": "Pedido não encontrado"},
    403: {"description": "Acesso negado"},
})
def buscar_pedidos(id: int, user=Depends(Authorization(['comum', 'adm'])), db: Session = Depends(db.get_db)):
    pedidos = service.pegar_pedidos_id(db, id)
    if not pedidos:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if user["nivel"] != "adm" and pedidos.id_cliente != int(user["sub"]):
        raise HTTPException(status_code=403, detail="Acesso negado")
    return pedidos

@router.delete("/{id}",  response_model=PedidoRemove, summary="Deletar pedido",
description="Remove um pedido existente com base no ID.",
responses={
    200: {"description": "Pedido deletado com sucesso"},
    404: {"description": "Pedido não encontrado"},
    403: {"description": "Acesso negado"},
})
def deletar_pedido(id: int, user=Depends(Authorization(['comum', 'adm'])), db: Session = Depends(db.get_db)):
    id_client = None
    if user["nivel"] != "adm":
        id_client = int(user["sub"])
    pedido = service.deletar_pedido(db, id, id_client)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"detail": 'Pedido deletado!'}


@router.put("/{id}", response_model=PedidoRead, summary="Atualizar pedido",
description="Atualiza completamente os dados de um pedido existente.",
responses={
    200: {"description": "Pedido atualizado com sucesso"},
    400: {"description": "Erro de validação"},
    404: {"description": "Pedido não encontrado"},
    403: {"description": "Acesso negado"},
}
)
def atualizar_pedido(id: int, pedido: PedidoCreate, user=Depends(Authorization(['comum', 'adm'])), db: Session = Depends(db.get_db)):
    try:
        id_client = None
        if user["nivel"] != "adm":
            id_client = int(user["sub"])
        pedido_atualizado = service.alterar_pedido(db, id, pedido, id_client)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not pedido_atualizado:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    return pedido_atualizado


@router.patch("/{id}", response_model=PedidoRead, dependencies=[Depends(Authorization(['adm']))], summary="Atualizar status do pedido",
description="Atualiza apenas o status de um pedido existente. Requer permissão de administrador.",
responses={
    200: {"description": "Status do pedido atualizado com sucesso"},
    404: {"description": "Pedido não encontrado"},
    403: {"description": "Acesso negado"},
})
def atualizar_status(id: int, status: PedidoStatus, db: Session = Depends(db.get_db)):
    pedido = service.patch_status_pedido(db, id, status)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido