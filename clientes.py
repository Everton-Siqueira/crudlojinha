from pydantic import BaseModel, Field, EmailStr, field_validator


#Model
class Clientes(BaseModel):
    nome_cliente: str = Field(min_length = 3)
    cidade: str = Field(min_length = 3)#minimo 3 caracteres
    email: EmailStr


    @field_validator("nome_cliente")
    def nome_deve_conter_espaco(cls, value: str) -> str:
        value = " ".join(value.strip().split())

        if " " not in value:
            raise ValueError("O nome deve conter ao menos um espaço.")

        return value

    
    



