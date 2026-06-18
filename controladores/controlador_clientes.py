from fastapi import APIRouter
from cliente import Cliente


#pip install sqlalchemy
from sqlalchemy import create_engine, text
router = APIRouter(prefix="/cliente", tags=["Cliente"])


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
            sql = """INSERT INTO public.cliente
                                (nome_cliente, email, cidade)
                        VALUES ( :nome_cliente, :email, :cidade)"""            
            dados = {
                "nome_cliente" : cliente.nome_cliente, #cliente . propriedade
                "email": cliente.email,
                "cidade": cliente.cidade
            }


            con.execute(text(sql), dados)
            con.commit() #confirma a transação
    except Exception as e:
        # Se der erro no banco, agora você verá o motivo real no Postman
        return {"status": "erro", "detalhe": str(e)}


#recovery =>consulta (getOne e getAll => pegar 1 ou pegar todos)
@router.get('/{id}')
def getOne(id: int ):
    
    engine = create_engine(DATABASE_URL)

    try:
        with engine.begin() as con:
            sql = """
                SELECT id, nome_cliente, email, cidade
                FROM public.cliente
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
                FROM public.cliente
                ORDER BY id
            """

            result = con.execute(text(sql))

            cliente = [dict(row._mapping) for row in result]

        return cliente

    except Exception as e:
        return {"erro": str(e)}
    


@router.put('/{id}')
def atualizar(id: int, cliente: Cliente):


    engine = create_engine(DATABASE_URL)
#logica do update
    try:
        with engine.begin() as con:

            sql = """
                UPDATE public.cliente
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
                DELETE FROM public.cliente
                WHERE id = :id
            """

            con.execute(text(sql), {"id": id})

        return {"mensagem": "Cliente deletado com sucesso", "id": id}

    except Exception as e:
        return {"erro": str(e)}
    
