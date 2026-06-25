from pydantic import BaseModel, Field

class Produto(BaseModel):
    nome: str = Field(min_length=2)
    preco: float = Field(gt=0)
    estoque: int = Field(ge=0)
    marca_id: int = Field(gt=0)
