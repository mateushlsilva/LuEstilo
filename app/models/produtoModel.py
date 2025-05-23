from sqlalchemy import Column, String, Float, Integer, Boolean, Date
from app.database import Base
from sqlalchemy.dialects.postgresql import ARRAY

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=True)
    codigo_barras = Column(String, nullable=False, index=True, unique=True)
    categoria = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    disponibilidade = Column(Boolean, default=True)
    descricao = Column(String, nullable=True)
    valor_venda = Column(Float, nullable=False)
    secao = Column(String, nullable=True)
    estoque_inicial = Column(Integer, default=0)
    data_validade = Column(Date, nullable=True)
    imagens = Column(ARRAY(String), nullable=True)
