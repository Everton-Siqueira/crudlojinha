from fastapi import APIRouter
from schemas import Marca
from banco_dados import DATABASE_URL


#pip install sqlalchemy
from sqlalchemy import create_engine, text
router = APIRouter(prefix="/marcas", tags=["Marcas"])



#crio a conexao
engine = create_engine(DATABASE_URL)

#REST
#Create
@router.post('/')
def cadastrar(marcas:Marcas):

    try:
        with engine.begin() as con: #inicializo a transação
            sql = """INSERT INTO public.marcas
                    (nome_marca, pais_origem)
	                VALUES (:nome, :pais_origem)""";                   
            
            dados = {
                "nome": marcas.nome_marca,
                "pais_origem": marcas.pais_origem
            }

            con.execute(text(sql), dados)

            return {"mensagem": "Marca cadastrada com sucesso"}

    except Exception as e:
        print(e)
        return {"erro": str(e), "detalhe": "Verifique os atributos da classe Marca"}


                  

#recovery =>consulta (getOne e getAll => pegar 1 ou pegar todos)
@router.get('/{id}')
def getOne(id: int ):
      
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
    
    try:
        with engine.begin() as con:

            sql = """
                SELECT id, nome_marca, pais_origem
	            FROM public.marcas
                ORDER BY id
            """

            result = con.execute(text(sql))

            lista_marcas = [dict(row._mapping) for row in result]

        return lista_marcas
    except Exception as e:
        return {"erro": str(e)}
    


@router.put('/{id}')
def atualizar(id: int, marcas: Marcas):
    
#logica do update
    try:
        with engine.begin() as con:

            sql = """
                UPDATE public.marcas
                SET nome_marca= :nome, pais_origem= :pais_origem
	            WHERE id = :id
            """

            dados = {
                "id": id,
                "nome": marcas.nome,
                "pais_origem": marcas.pais_origem
            }

            result = con.execute(text(sql), dados)

            return {"mensagem": "Marca atualizada com sucesso"}

    except Exception as e:
        return {"erro": str(e)}
    
    

@router.delete("/{id}")
def deletar(id: int):
    
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
    
