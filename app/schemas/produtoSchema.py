from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ProdutoBase(BaseModel):
    categoria: str
    preco: float
    disponibilidade: Optional[bool] = True
    descricao: Optional[str]
    valor_venda: float
    codigo_barras: str
    secao: Optional[str]
    estoque_inicial: int
    data_validade: Optional[date]
    imagens: Optional[List[str]]


class ProdutoRemove(BaseModel):
    detail: str

class ProdutoRead(ProdutoBase):
    id: int

    class Config:
        orm_mode = True
