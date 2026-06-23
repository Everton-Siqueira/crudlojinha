from pydantic import BaseModel, Field

class Itens_Compras(BaseModel):
    pedido_id: int = Field(gt=0)
    produto_id: int = Field(gt=0)
    quantidade: int = Field(gt=0)
    preco_unitario: float = Field(gt=0)