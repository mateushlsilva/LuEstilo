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

    def pegar_todos_produtos(self):
        pass

    def pegar_produto_id(self):
        pass

    def alterar_produto(self):
        pass

    def deletar_produto(self):
        pass