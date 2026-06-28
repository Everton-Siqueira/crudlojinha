from pydantic import BaseModel, Field

# Schema de Cliente
class Cliente(BaseModel):
    nome: str = Field(min_length=2)
    email: str
    cidade: str

# Schema de Produto
class Produto(BaseModel):
    nome: str = Field(min_length=2)
    preco: float = Field(gt=0)
    estoque: int = Field(ge=0)
    marca_id: int = Field(gt=0)

# Schema de Marca
class Marca(BaseModel):
    nome_marca: str = Field(min_length=2)
    pais_origem: str = Field(min_length=2)
    
# Schema de Pedido
class Pedido(BaseModel):
    data_pedido: str
    status: str
    cliente_id: int = Field(gt=0)

# Schema de Item de Compra
class ItemCompra(BaseModel):
    quantidade: int = Field(gt=0)
    pedido_id: int = Field(gt=0)
    produto_id: int = Field(gt=0)