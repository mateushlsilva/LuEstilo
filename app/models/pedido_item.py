from sqlalchemy import Column, String, Integer, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class PedidoItem(Base):
    __tablename__ = "pedido_itens"

    id_item = Column(Integer, primary_key=True, autoincrement=True)
    id_pedido = Column(Integer, ForeignKey("pedidos.id_pedido"), nullable=False)
    id_produto = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)

    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto")
