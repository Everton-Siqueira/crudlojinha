from pydantic import BaseModel, Field
from datetime import date

class Pedido(BaseModel):
    cliente_id: int = Field(gt=0)
    data_pedido: date
    status: str = Field(min_length=3, max_length=50)