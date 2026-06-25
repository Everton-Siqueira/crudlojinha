from fastapi import APIRouter
from pedidos import Pedidos


#pip install sqlalchemy
from sqlalchemy import create_engine, text
router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


#inserção no banco "postgresql://usuario:senha@servidor:porta/banco"
DATABASE_URL = "postgresql://postgres:123@localhost:5432/crudlojinha"

#crio a conexao
engine = create_engine(DATABASE_URL)

#REST
#Create
@router.post('/')
def cadastrar(pedidos:Pedidos):

    try:
        with engine.begin() as con: #inicializo a transação
            sql = """INSERT INTO public.pedidos
                    (cliente_id, data_pedido, status)
	                VALUES (:cliente_id, COALESCE(:data_pedido, CURRENT_DATE), :status)""";                   
            
            dados = {
                "cliente_id": str(pedidos.cliente_id),
                "data_pedido": pedidos.data_pedido,
                "status": pedidos.status
            }

            con.execute(text(sql), dados)

            return {"mensagem": "Pedido cadastrado com sucesso"}

    except Exception as e:
        print(e)
        return {"erro": str(e), "detalhe": "Verifique os atributos da classe Pedido"}        

#recovery =>consulta (getOne e getAll => pegar 1 ou pegar todos)
@router.get('/{id}')
def getOne(id: int ):

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

            lista_pedidos = [dict(row._mapping) for row in result]

        return lista_pedidos

    except Exception as e:
        return {"erro": str(e)}
    


@router.put('/{id}')
def atualizar(id: int, pedidos: Pedidos):

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
                "cliente_id": pedidos.cliente_id,
                "data_pedido": pedidos.data_pedido,
                "status": pedidos.status
            }

            result = con.execute(text(sql), dados)

            return {"mensagem": "Pedido atualizado com sucesso"}

    except Exception as e:
        return {"erro": str(e)}
    
    

@router.delete("/{id}")
def deletar(id: int):
    
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
    
