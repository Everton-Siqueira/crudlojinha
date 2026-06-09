import uvicorn
from fastapi import FastAPI


from controlador_clientes import router as clientes_router


app = FastAPI()


app.include_router(clientes_router)



if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        port = 80,
        reload = True
    )
