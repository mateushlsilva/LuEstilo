from sqlalchemy.orm import Session
from app.models.pedidoModel import Pedido
from app.models.pedido_item import PedidoItem
from app.models.produtoModel import Produto
from app.schemas.pedidoSchema import PedidoBase, PedidoRead, PedidoCreate
from typing import Optional
from fastapi import HTTPException

class PedidoService:
    def __init__(self):
        pass

    def criar_pedido(self, db: Session, pedido_data: PedidoCreate):
        for item in pedido_data.itens:
            produto = db.query(Produto).filter(Produto.id == item.id_produto).first()
            if not produto:
                raise HTTPException(status_code=404, detail=f"Produto {item.id_produto} não encontrado.")
            if produto.estoque_inicial < item.quantidade:
                raise HTTPException(status_code=409, detail=f"Estoque insuficiente para o produto {produto.codigo_barras}.")

        novo_pedido = Pedido(
            id_cliente=pedido_data.id_cliente,
            status=pedido_data.status,
            periodo=pedido_data.periodo,
            secao_produtos=pedido_data.secao_produtos
        )
        db.add(novo_pedido)
        db.flush()  

       
        for item in pedido_data.itens:
            novo_pedido_item = PedidoItem(
                id_pedido=novo_pedido.id_pedido,
                id_produto=item.id_produto,
                quantidade=item.quantidade
            )
            db.add(novo_pedido_item)
            produto = db.query(Produto).filter(Produto.id == item.id_produto).first()
            produto.estoque_inicial -= item.quantidade

        db.commit()
        db.refresh(novo_pedido)
        return novo_pedido

    def pegar_todos_pedidos(self):
        pass

    def pegar_pedidos_id(self):
        pass

    def alterar_pedido(self): 
        pass

    def deletar_pedido(self):
        pass