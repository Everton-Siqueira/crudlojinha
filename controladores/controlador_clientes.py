from fastapi import APIRouter
from clientes import Clientes


#pip install sqlalchemy
from sqlalchemy import create_engine, text
router = APIRouter(prefix="/cliente", tags=["Clientes"])


#inserção no banco "postgresql://usuario:senha@servidor:porta/banco"
DATABASE_URL = "postgresql://postgres:123@localhost:5432/crudlojinha"


#REST
#Create
@router.post('/')
def cadastrar(cliente: Cliente): #observe o tipo que é meu model

    #crio a conexao
    engine = create_engine(DATABASE_URL)


    try:
        with engine.begin() as con: #inicializo a transação
            sql = """INSERT INTO public.clientes
                                (nome_cliente, email, cidade)
                        VALUES ( :nomezinho, :email, :cidade)"""            
            dados = {
                "nomezinho" : cliente.nome, #cliente . propriedade
                "email": cliente.email,
                "cidade": cliente.cidade
            }


            con.execute(text(sql), dados)
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
                SELECT id, nome_cliente, email, cidade
                FROM public.clientes
                WHERE id = :id
            """

            result = con.execute(text(sql), {"id": id}).fetchone()

            if result is None:
                return {"erro": "Cliente não encontrado"}

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
                SELECT id, nome_cliente, email, cidade
                FROM public.clientes
                ORDER BY id
            """

            result = con.execute(text(sql))

            clientes = [dict(row._mapping) for row in result]

        return clientes

    except Exception as e:
        return {"erro": str(e)}
    


@router.put('/{id}')
def atualizar(id: int, cliente: Cliente):


    engine = create_engine(DATABASE_URL)
#logica do update
    try:
        with engine.begin() as con:

            sql = """
                UPDATE public.clientes
                SET nome_cliente = :nome_cliente,
                    email = :email,
                    cidade = :cidade
                WHERE id = :id
            """

            dados = {
                "id": id,
                "nome_cliente": cliente.nome,
                "email": cliente.email,
                "cidade": cliente.cidade
            }

            result = con.execute(text(sql), dados)

            return {"mensagem": "Cliente atualizado com sucesso"}

    except Exception as e:
        return {"erro": str(e)}
    
    

@router.delete("/{id}")
def deletar(id: int):
    engine = create_engine(DATABASE_URL)

    try:
        with engine.begin() as con:
            sql = """
                DELETE FROM public.clientes
                WHERE id = :id
            """

            con.execute(text(sql), {"id": id})

        return {"mensagem": "Cliente deletado com sucesso", "id": id}

    except Exception as e:
        return {"erro": str(e)}
    
