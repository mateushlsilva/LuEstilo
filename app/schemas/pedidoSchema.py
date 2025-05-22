from pydantic import BaseModel
from typing import Optional
from app.schemas import clienteSchema, produtoSchema


class PedidoBase(BaseModel):
    periodo: Optional[str]
    secao_produtos: Optional[str]
    status: str

class PedidoCreate(PedidoBase):
    id_cliente: int
    id_produto: int

class PedidoRead(PedidoBase):
    id_pedido: int
    cliente: clienteSchema.ClienteRead
    produto: produtoSchema.ProdutoRead

    class Config:
        orm_mode = True