import uvicorn
from fastapi import FastAPI


from controladores.controlador_clientes import router as clientes_router
from controladores.controlador_produto import router as produto_router
from controladores.controlador_marcas import router as marcas_router
from controladores.controlador_pedidos import router as pedidos_router
from controladores.controlador_itens_compras import router as itens_compras

from clientes import Clientes
from produto import Produto
from marcas import Marcas
from pedidos import Pedidos
from itens_compras import Itens_Compras

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API da CrudLojinha!", "status": "ok"}

app.include_router(clientes_router)
app.include_router(produto_router)
app.include_router(marcas_router)
app.include_router(pedidos_router)
app.include_router(itens_compras)



Clientes.model_rebuild()
Produto.model_rebuild()
Marcas.model_rebuild()
Pedidos.model_rebuild()
Itens_Compras.model_rebuild()

if __name__ == '__main__':
    # Lê a porta que o Render vai te dar (padrão 10000 no Render se não achar)
    port = int(os.getenv("PORT", 8000)) 
    
    uvicorn.run(
        'main:app',
        host='0.0.0.0', # Importante: mude para 0.0.0.0 para aceitar conexões externas
        port=port,
        reload=False # Desative o reload em produção no Render
    )