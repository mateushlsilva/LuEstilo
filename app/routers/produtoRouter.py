from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import Database
from app.schemas.produtoSchema import ProdutoBase, ProdutoRead
from app.services.produtoService import ProdutoService
from app.models.produtoModel import Produto
from app.utils.validated import Validadores

router = APIRouter(prefix="/produtos", tags=["Produtos"])
service = ProdutoService()
db = Database()


@router.post("/", response_model=ProdutoRead)
def criar_cliente(produto: ProdutoBase, db: Session = Depends(db.get_db)):
   
    if db.query(Produto).filter_by(codigo_barras=produto.codigo_barras).first():
        raise HTTPException(status_code=400, detail="Código de barras já cadastrado!")

    novo_produto = service.criar_produto(db, produto)
    return novo_produto