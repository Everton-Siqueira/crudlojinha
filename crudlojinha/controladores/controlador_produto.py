from fastapi import APIRouter, HTTPException
from schemas import Produto
from banco_dados import DATABASE_URL


#pip install sqlalchemy
from sqlalchemy import create_engine, text
router = APIRouter(prefix="/produto", tags=["Produtos"])



#crio a conexao
engine = create_engine(DATABASE_URL) # criando aqui para usar em todas as funções, evitando criar uma nova conexão a cada função(rotas)

#REST
#Create
@router.post('/')
def cadastrar(produto:Produto):
   
    try:
        with engine.begin() as con: #inicializo a transação
            sql = """INSERT INTO public.produto
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
        print("ERRO DETECTADO:", e)
        # IMPORTANTE: Retorna o erro para o Postman não receber 'null' com Status 200
        return {"erro": str(e), "detalhe": "Verifique os atributos da classe Produto"}
        
          

#recovery =>consulta (getOne e getAll => pegar 1 ou pegar todos)
@router.get('/{id}')
def getOne(id: int ):
    
    try:
        with engine.begin() as con:
            sql = """
                SELECT id, nome_produto, preco, estoque, marca_id
	            FROM public.produto
                WHERE id = :id
            """

            result = con.execute(text(sql), {"id": id}).fetchone()

            if result is None:
                raise HTTPException(status_code=404, detail="Produto não encontrado")

            return dict(result._mapping)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        return {"erro": str(e)}
    
@router.get('/')
def todos():
        
    try:
        with engine.begin() as con:

            sql = """
                SELECT id, nome_produto, preco, estoque, marca_id
	            FROM public.produto
                ORDER BY id
            """

            result = con.execute(text(sql))

            produto = [dict(row._mapping) for row in result]

        return produto

    except Exception as e:
        return {"erro": str(e)}
    


@router.put('/{id}')
def atualizar(id: int, produto: Produto):
    
#logica do update
    try:
        with engine.begin() as con:

            sql = """
                UPDATE public.produto
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
        print("ERRO NO BANCO DE DADOS:", e)
        return {"erro": str(e)} # Retorna o erro no Postman para facilitar a identificação do problema 

 
@router.delete("/{id}")
def deletar(id: int):
    
    try:
        with engine.begin() as con:
            sql = """
                DELETE FROM public.produto
                WHERE id = :id
                
            """

            con.execute(text(sql), {"id": id})

        return {"mensagem": "Produto deletado com sucesso", "id": id}

    except Exception as e:
        return {"erro": str(e)}
    
