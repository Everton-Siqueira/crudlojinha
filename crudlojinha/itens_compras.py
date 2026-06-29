from sqlalchemy import Column, Integer, ForeignKey
from banco_dados import Base

class Itens_ComprasTabela(Base):
    __tablename__ = "itens_compras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantidade = Column(Integer, nullable=False)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produto.id", ondelete="CASCADE"), nullable=False)