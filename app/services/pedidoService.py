from sqlalchemy.orm import Session
from app.models.pedidoModel import Pedido
from app.models.pedido_item import PedidoItem
from app.models.produtoModel import Produto
from app.models.clientesModel import Cliente
from app.schemas.pedidoSchema import PedidoBase, PedidoRead, PedidoCreate, PedidoStatus
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

    def pegar_todos_pedidos(
        self,
        db: Session,
        periodo: Optional[str],
        secao_produtos: Optional[str],
        id_pedido: Optional[int],
        status: Optional[str],
        cliente: Optional[str],
        cliente_id: Optional[int],
        skip: int,
        limit: int
    ):
        query = db.query(Pedido)

        filtros = {
            Pedido.periodo.ilike(f"%{periodo}%") if periodo else None,
            Pedido.secao_produtos.ilike(f"%{secao_produtos}%") if secao_produtos else None,
            Pedido.id_pedido == id_pedido if id_pedido else None,
            Pedido.status.ilike(f"%{status}%") if status else None,
        }

        for filtro in filtros:
            if filtro is not None:
                query = query.filter(filtro)
        
        if cliente_id:
            query = query.filter(Pedido.id_cliente == cliente_id)

        elif cliente:
            query = query.join(Pedido.cliente).filter(Cliente.nome.ilike(f"%{cliente}%"))

        return query.offset(skip).limit(limit).all()

    def pegar_pedidos_id(self, db: Session, id: int):
        return db.query(Pedido).filter(Pedido.id_pedido == id).first()

    def alterar_pedido(self, db: Session, id: int, dados: PedidoCreate, id_client: Optional[int]): 
        pedido = db.query(Pedido).filter(Pedido.id_pedido == id).first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        if id_client != None and pedido.id_cliente != id_client:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        if dados.periodo is not None:
            pedido.periodo = dados.periodo
        if dados.secao_produtos is not None:
            pedido.secao_produtos = dados.secao_produtos
        if dados.status is not None:
            pedido.status = dados.status

        
        itens_atuais = {item.id_produto: item for item in pedido.itens}

        
        novos_itens = {item.id_produto: item for item in dados.itens}

        
        for prod_id in list(itens_atuais):
            if prod_id not in novos_itens:
                item = itens_atuais[prod_id]
                produto = db.query(Produto).filter(Produto.id == prod_id).first()
                if produto:
                    produto.estoque_inicial += item.quantidade
                db.delete(item)

        
        for prod_id, novo_item in novos_itens.items():
            produto = db.query(Produto).filter(Produto.id == prod_id).first()
            if not produto:
                raise HTTPException(status_code=404, detail=f"Produto {prod_id} não encontrado")

            existente = itens_atuais.get(prod_id)
            if existente:
                diff = novo_item.quantidade - existente.quantidade
                if produto.estoque_inicial < diff:
                    raise HTTPException(status_code=400, detail=f"Estoque insuficiente para {produto.codigo_barras}")
                produto.estoque_inicial -= diff
                existente.quantidade = novo_item.quantidade
            else:
                if produto.estoque_inicial < novo_item.quantidade:
                    raise HTTPException(status_code=400, detail=f"Estoque insuficiente para {produto.codigo_barras}")
                produto.estoque_inicial -= novo_item.quantidade
                novo = PedidoItem(
                    id_pedido=id,
                    id_produto=prod_id,
                    quantidade=novo_item.quantidade
                )
                db.add(novo)

        db.commit()
        db.refresh(pedido)
        return pedido

    def deletar_pedido(self, db: Session, id: int, id_client: Optional[int]):
        pedido = db.query(Pedido).filter(Pedido.id_pedido == id).first()
        if not pedido:
            return None
        if id_client != None and pedido.id_cliente != id_client:
            raise HTTPException(status_code=403, detail="Acesso negado")

        db.delete(pedido)
        db.commit()
        return True
    
    def patch_status_pedido(self, db: Session, id: int, status: PedidoStatus):
        pedido = db.query(Pedido).filter(Pedido.id_pedido == id).first()
        if not pedido:
            return None
        pedido.status = status.status
        db.commit()
        db.refresh(pedido)
        return pedido
