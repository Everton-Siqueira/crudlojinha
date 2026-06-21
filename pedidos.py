from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class Pedidos(BaseModel):
    cliente_id: int = Field(gt=0)
    data_pedido: Optional[date] = None
    status: str = Field(min_length=3, max_length=50)

    
