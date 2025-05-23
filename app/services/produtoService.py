from sqlalchemy.orm import Session
from app.models.produtoModel import Produto
from app.schemas.produtoSchema import ProdutoBase, ProdutoRead
from typing import Optional

class ProdutoService:
    def __init__(self):
        pass

    def criar_produto(self, db: Session, produto: ProdutoBase):
        novo_produto = Produto(
            categoria=produto.categoria,
            codigo_barras=produto.codigo_barras,
            data_validade=produto.data_validade,
            descricao=produto.descricao,
            disponibilidade=produto.disponibilidade,
            estoque_inicial=produto.estoque_inicial,
            imagens=produto.imagens,
            preco=produto.preco,
            secao=produto.secao,
            valor_venda=produto.valor_venda
        )
        db.add(novo_produto)
        db.commit()
        db.refresh(novo_produto)
        return novo_produto

    def pegar_todos_produtos(
        self,
        db: Session,
        categoria: Optional[str], 
        preco: Optional[float] , 
        disponibilidade: Optional[bool],
        skip: int,
        limit: int
    ):
        query = db.query(Produto)

        if categoria:
            query = query.filter(Produto.categoria.ilike(f"%{categoria}%"))
        if preco is not None:
            query = query.filter(Produto.preco <= preco).order_by(Produto.preco.desc())
        if disponibilidade is not None:
            query = query.filter(Produto.disponibilidade==disponibilidade)

        
        return query.offset(skip).limit(limit).all()

    def pegar_produto_id(self):
        pass

    def alterar_produto(self):
        pass

    def deletar_produto(self):
        pass