from datetime import datetime, timezone
from app.database import Database
from app.models.clientesModel import Cliente
from app.models.produtoModel import Produto
from app.models.pedidoModel import Pedido
from app.models.pedido_item import PedidoItem
from app.utils.auth import Auth


def criar_admin():
    auth = Auth()
    senha = auth.hash_senha("admin")

    db_gen = Database().get_db()
    db = next(db_gen)

    try:
        admin = db.query(Cliente).filter_by(email="admin@admin.com").first()
        if not admin:
            admin = Cliente(
                nome='admin',
                email='admin@admin.com',
                cpf='12345678911',
                telefone='12345678911',
                senha=senha,
                nivel='adm'
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("Admin criado.")
        else:
            print("Admin já existe.")

        produto = db.query(Produto).filter_by(nome="Produto Exemplo").first()
        if not produto:
            produto = Produto(
                categoria="Roupas",
                codigo_barras="1234567890123",
                data_validade=None,
                descricao="Produto exemplo de inicialização",
                disponibilidade=True,
                estoque_inicial=50,
                imagens=["https://gnwpedhdpqaxfxzwktsg.supabase.co/storage/v1/object/public/imagens//images.jpeg"],
                preco=49.90,
                secao="Masculino",
                valor_venda=59.90,
                nome="Produto Exemplo"
            )
            db.add(produto)
            db.commit()
            db.refresh(produto)
            print("Produto criado.")
        else:
            print("Produto já existe.")

        pedido_existente = db.query(Pedido).filter_by(id_cliente=admin.id).first()
        if not pedido_existente:
            if produto.estoque_inicial >= 2:
                novo_pedido = Pedido(
                    id_cliente=admin.id,
                    status="pendente",
                    periodo=datetime.now(timezone.utc),
                    secao_produtos=produto.secao 
                )
                db.add(novo_pedido)
                db.flush()  

                item_pedido = PedidoItem(
                    id_pedido=novo_pedido.id_pedido,
                    id_produto=produto.id,
                    quantidade=2
                )
                db.add(item_pedido)

                # Atualiza o estoque
                produto.estoque_inicial -= 2

                db.commit()
                db.refresh(novo_pedido)
                print("Pedido criado.")
            else:
                print("Estoque insuficiente para criar pedido de exemplo.")
        else:
            print("Pedido de exemplo já existe.")
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass

if __name__ == '__main__':
    criar_admin()