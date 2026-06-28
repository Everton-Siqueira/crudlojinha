from sqlalchemy import Column, Integer, String
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome_cliente = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)  



