import os
import uvicorn
from fastapi import FastAPI

# 1. Importa o engine e a Base do seu arquivo banco_dados.py
from banco_dados import engine, Base  

# 2. Importa os modelos para o SQLAlchemy saber quais tabelas criar
import clientes
import marcas
import pedidos
import produto
import itens_compras

from controladores.controlador_clientes import router as clientes_router
from controladores.controlador_produto import router as produto_router
from controladores.controlador_marcas import router as marcas_router
from controladores.controlador_pedidos import router as pedidos_router
from controladores.controlador_itens_compras import router as itens_compras_router

app = FastAPI()

# 3. Esta linha cria todas as tabelas no banco de dados caso elas não existam
Base.metadata.create_all(bind=engine)

# 3. Esta linha força a exclusão das tabelas antigas e desatualizadas
#Base.metadata.drop_all(bind=engine)

# Esta linha cria todas as tabelas novas com as colunas corretas
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {
        "message": "Bem-vindo à API da CrudLojinha!",
        "status": "ok"
    }

app.include_router(clientes_router)
app.include_router(produto_router)
app.include_router(marcas_router)
app.include_router(pedidos_router)
app.include_router(itens_compras_router)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)