from fastapi import APIRouter
from schemas import Cliente
from banco_dados import DATABASE_URL

from sqlalchemy import create_engine, text

router = APIRouter(prefix="/clientes", tags=["Clientes"])

engine = create_engine(DATABASE_URL)


# CREATE
@router.post("/")
def cadastrar(cliente: Cliente):

    try:
        with engine.begin() as con:
            sql = """
                INSERT INTO public.clientes
                (nome_cliente, email, cidade)
                VALUES (:nome_cliente, :email, :cidade)
            """

            con.execute(text(sql), {
                "nome_cliente": cliente.nome_cliente,
                "email": cliente.email,
                "cidade": cliente.cidade
            })

        return {"mensagem": "Cliente cadastrado com sucesso"}

    except Exception as e:
        return {"erro": str(e)}


# GET ONE
@router.get("/{id}")
def getOne(id: int):

    try:
        with engine.begin() as con:
            sql = """
                SELECT id, nome_cliente, email, cidade
                FROM public.clientes
                WHERE id = :id
            """

            result = con.execute(text(sql), {"id": id}).fetchone()

            if not result:
                return {"erro": "Cliente não encontrado"}

            return dict(result._mapping)

    except Exception as e:
        return {"erro": str(e)}


# GET ALL
@router.get("/")
def todos():

    try:
        with engine.begin() as con:
            sql = """
                SELECT id, nome_cliente, email, cidade
                FROM public.clientes
                ORDER BY id
            """

            result = con.execute(text(sql))

            return [dict(row._mapping) for row in result]

    except Exception as e:
        return {"erro": str(e)}


# UPDATE
@router.put("/{id}")
def atualizar(id: int, cliente: Cliente):

    try:
        with engine.begin() as con:
            sql = """
                UPDATE public.clientes
                SET nome_cliente = :nome_cliente,
                    email = :email,
                    cidade = :cidade
                WHERE id = :id
            """

            con.execute(text(sql), {
                "id": id,
                "nome_cliente": cliente.nome,
                "email": cliente.email,
                "cidade": cliente.cidade
            })

        return {"mensagem": "Cliente atualizado com sucesso"}

    except Exception as e:
        return {"erro": str(e)}


# DELETE
@router.delete("/{id}")
def deletar(id: int):

    try:
        with engine.begin() as con:
            sql = """
                DELETE FROM public.clientes
                WHERE id = :id
            """

            con.execute(text(sql), {"id": id})

        return {"mensagem": "Cliente deletado com sucesso"}

    except Exception as e:
        return {"erro": str(e)}