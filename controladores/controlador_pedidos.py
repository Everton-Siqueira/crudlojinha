from fastapi import APIRouter
from pedido import Pedido


#pip install sqlalchemy
from sqlalchemy import create_engine, text
router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


#inserção no banco "postgresql://usuario:senha@servidor:porta/banco"
DATABASE_URL = "postgresql://postgres:123@localhost:5432/crudlojinha"


#REST
#Create
@router.post('/')
def cadastrar(pedido:Pedido):

    #crio a conexao
    engine = create_engine(DATABASE_URL)


    try:
        with engine.begin() as con: #inicializo a transação
            sql = """INSERT INTO public.pedidos
                    (cliente_id, data_pedido, status)
	                VALUES (:cliente_id, :data_pedido, :status)""";                   
            
            dados = {
                "cliente_id": pedido.cliente_id,
                "data_pedido": pedido.data_pedido,
                "status": pedido.status
            }

            con.execute(text(sql), dados)

            return {"mensagem": "Pedido cadastrado com sucesso"}

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
                SELECT id, cliente_id, data_pedido, status
	            FROM public.pedidos
                WHERE id = :id
            """

            result = con.execute(text(sql), {"id": id}).fetchone()

            if result is None:
                return {"erro": "Pedido não encontrado"}

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
                SELECT id, cliente_id, data_pedido, status
	            FROM public.pedidos
                ORDER BY id
            """

            result = con.execute(text(sql))

            clientes = [dict(row._mapping) for row in result]

        return clientes

    except Exception as e:
        return {"erro": str(e)}
    


@router.put('/{id}')
def atualizar(id: int, pedido: Pedido):


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
                DELETE FROM public.pedidos
                WHERE id = :id
                
            """

            con.execute(text(sql), {"id": id})

        return {"mensagem": "Pedido deletado com sucesso", "id": id}

    except Exception as e:
        return {"erro": str(e)}
    
