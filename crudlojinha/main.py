import uvicorn
from fastapi import FastAPI


from controladores.controlador_clientes import router as clientes_router
from controladores.controlador_produto import router as produto_router
from controladores.controlador_marcas import router as marcas_router
from controladores.controlador_pedidos import router as pedidos_router
from controladores.controlador_itens_compras import router as itens_compras


app = FastAPI()


app.include_router(clientes_router)
app.include_router(produto_router)
app.include_router(marcas_router)
app.include_router(pedidos_router)
app.include_router(itens_compras)





if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        port = 80,
        reload = True
    )
