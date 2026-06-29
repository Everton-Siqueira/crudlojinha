from sqlalchemy import Column, Integer, String
from banco_dados import Base

class MarcaTabela(Base):
    __tablename__ = "marcas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_marca = Column(String(255), nullable=False)
    pais_origem = Column(String(100), nullable=False)