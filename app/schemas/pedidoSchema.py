from pydantic import BaseModel
from typing import Optional, List
from app.schemas import clienteSchema, produtoSchema


class PedidoBase(BaseModel):
    periodo: Optional[str]
    secao_produtos: Optional[str]
    status: str

class PedidoItemCreate(BaseModel):
    id_produto: int
    quantidade: int

class PedidoCreate(PedidoBase):
    id_cliente: int
    periodo: Optional[str]
    status: str
    itens: List[PedidoItemCreate]

class PedidoItemRead(BaseModel):
    produto: produtoSchema.ProdutoRead
    quantidade: int

    class Config:
        orm_mode = True

class PedidoRemove(BaseModel):
    detail: str

class PedidoRead(PedidoBase):
    id_pedido: int
    cliente: clienteSchema.ClienteRead
    itens: List[PedidoItemRead]

    class Config:
        orm_mode = True