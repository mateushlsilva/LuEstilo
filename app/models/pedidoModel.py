from sqlalchemy import Column, String, Integer, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedido = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    id_produto = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    periodo = Column(String, nullable=True)
    secao_produtos = Column(String, nullable=True)
    status = Column(String, nullable=False)
    cliente = relationship("Cliente")
    produto = relationship("Produto")
