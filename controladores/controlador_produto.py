from fastapi import APIRouter
from produto import Produto


#pip install sqlalchemy
from sqlalchemy import create_engine, text
router = APIRouter(prefix="/produto", tags=["Produtos"])


#inserção no banco "postgresql://usuario:senha@servidor:porta/banco"
DATABASE_URL = "postgresql://postgres:123@localhost:5432/crudlojinha"


#REST
#Create
@router.post('/')
def cadastrar(produto:Produto):

    #crio a conexao
    engine = create_engine(DATABASE_URL)


    try:
        with engine.begin() as con: #inicializo a transação
            sql = """INSERT INTO public.produtos
                         (nome_produto, preco, estoque, marca_id)
	                    VALUES (:nome, :preco, :estoque, :marca_id)""";                   
            
            dados = {
                "nome" : produto.nome,
                "preco" : produto.preco,
                "estoque" : produto.estoque,
                "marca_id" : produto.marca_id
                
            }

          

            con.execute(text(sql), dados)

            return {"mensagem": "Produto cadastrado com sucesso"}

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
                SELECT id, nome_produto, preco, estoque, marca_id
	            FROM public.produtos
                WHERE id = :id
            """

            result = con.execute(text(sql), {"id": id}).fetchone()

            if result is None:
                return {"erro": "Produto não encontrado"}

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
                SELECT id, nome_produto, preco, estoque, marca_id
	            FROM public.produtos
                ORDER BY id
            """

            result = con.execute(text(sql))

            clientes = [dict(row._mapping) for row in result]

        return clientes

    except Exception as e:
        return {"erro": str(e)}
    


@router.put('/{id}')
def atualizar(id: int, produto: Produto):


    engine = create_engine(DATABASE_URL)
#logica do update
    try:
        with engine.begin() as con:

            sql = """
                UPDATE public.produtos
	            SET nome_produto= :nome_produto, preco= :preco, estoque= :estoque, marca_id= :marca_id
	            WHERE id = :id
            """

            dados = {
                "id": id,
                "nome_produto": produto.nome,
                "preco": produto.preco,
                "estoque": produto.estoque,
                "marca_id": produto.marca_id
            }

            result = con.execute(text(sql), dados)

            return {"mensagem": "Produto atualizado com sucesso"}

    except Exception as e:
        return {"erro": str(e)}
    
    

@router.delete("/{id}")
def deletar(id: int):
    engine = create_engine(DATABASE_URL)

    try:
        with engine.begin() as con:
            sql = """
                DELETE FROM public.produtos 
                WHERE id = :id
                
            """

            con.execute(text(sql), {"id": id})

        return {"mensagem": "Produto deletado com sucesso", "id": id}

    except Exception as e:
        return {"erro": str(e)}
    
