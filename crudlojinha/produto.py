from sqlalchemy import Column, Integer, String, Numeric
from banco_dados import Base  

class ProdutoTabela(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_produto = Column(String(255), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    estoque = Column(Integer, nullable=False)
    marca_id = Column(Integer, nullable=True)