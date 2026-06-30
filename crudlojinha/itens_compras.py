from sqlalchemy import Column, Integer, ForeignKey, numeric
from banco_dados import Base

class Itens_ComprasTabela(Base):
    __tablename__ = "itens_compras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantidade = Column(Integer, nullable=False)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produto.id", ondelete="CASCADE"), nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False, server_default="0.00")