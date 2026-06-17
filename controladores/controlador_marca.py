from fastapi import APIRouter
from pedido import Pedido


#pip install sqlalchemy
from sqlalchemy import create_engine, text
router = APIRouter(prefix="/marcas", tags=["Marcas"])


#inserção no banco "postgresql://usuario:senha@servidor:porta/banco"
DATABASE_URL = "postgresql://postgres:123@localhost:5432/lojinha"


#REST
#Create
@router.post('/')
def cadastrar(marca:Marca):

    #crio a conexao
    engine = create_engine(DATABASE_URL)


    try:
        with engine.begin() as con: #inicializo a transação
            sql = """INSERT INTO public.marcas
                    (nome_marca, pais_origem)
	                VALUES (:nome, :pais_origem)""";                   
            
            dados = {
                "nome": marca.nome,
                "pais_origem": marca.pais_origem
            }

            con.execute(text(sql), dados)

            return {"mensagem": "Marca cadastrada com sucesso"}

    except Exception as e:
        print(e)
    engine.dispose()
    
                  

#recovery =>consulta (getOne e getAll => pegar 1 ou pegar todos)
@router.get('/{id}')
def getOne(id: int ):
    
    engine = create_engine(DATABASE_URL)

    try:
        with engine.begin() as con:
            sql = """
                SELECT id, nome_marca, pais_origem
	            FROM public.marcas
                WHERE id = :id
            """

            result = con.execute(text(sql), {"id": id}).fetchone()

            if result is None:
                return {"erro": "Marca não encontrada"}

            return dict(result._mapping)

    except Exception as e:
        return {"erro": str(e)}
    return {} #um elemento


#postman http://localhost/cliente/todos
@router.get('/')
def todos():
    engine = create_engine(DATABASE_URL)

    try:
        with engine.begin() as con:

            sql = """
                SELECT id, nome_marca, pais_origem
	            FROM public.marcas
                ORDER BY id
            """

            result = con.execute(text(sql))

            clientes = [dict(row._mapping) for row in result]

        return clientes

    except Exception as e:
        return {"erro": str(e)}
    


@router.put('/{id}')
def atualizar(id: int, marca: Marca):


    engine = create_engine(DATABASE_URL)
#logica do update
    try:
        with engine.begin() as con:

            sql = """
                UPDATE public.pedidos
	            SET cliente_id=:cliente_id, data_pedido=:data_pedido, status=:status    
	            WHERE id = :id
            """

            dados = {
                "id": id,
                "cliente_id": pedido.cliente_id,
                "data_pedido": pedido.data_pedido,
                "status": pedido.status
            }

            result = con.execute(text(sql), dados)

            return {"mensagem": "Pedido atualizado com sucesso"}

    except Exception as e:
        return {"erro": str(e)}
    
    

@router.delete("/{id}")
def deletar(id: int):
    engine = create_engine(DATABASE_URL)

    try:
        with engine.begin() as con:
            sql = """
                DELETE FROM public.marcas
                WHERE id = :id
                
            """

            con.execute(text(sql), {"id": id})

        return {"mensagem": "Marca deletada com sucesso", "id": id}

    except Exception as e:
        return {"erro": str(e)}
    
