from sqlalchemy import Column, Integer, String, ForeignKey
from banco_dados import Base

class PedidoTabela(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_pedido = Column(String(50), nullable=False)  # Ou DateTime se preferir
    status = Column(String(50), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)