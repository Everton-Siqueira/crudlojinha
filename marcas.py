from pydantic import BaseModel, Field

class Marcas(BaseModel):
    id: int | None = None
    nome_marca: str = Field(min_length=2, max_length=100)
    pais_origem: str = Field(min_length=2, max_length=100)