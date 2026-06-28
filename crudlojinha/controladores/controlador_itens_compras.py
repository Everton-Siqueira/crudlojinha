from fastapi import APIRouter
from schemas import Itens_Compra
from banco_dados import DATABASE_URL

#pip install sqlalchemy
from sqlalchemy import create_engine, text
router = APIRouter(prefix="/itens_compras", tags=["Itens de Compras"])


#crio a conexao

engine = create_engine(DATABASE_URL)

#REST
#Create
@router.post('/')
def cadastrar(itens_compra: Itens_Compras):

    try:
        with engine.begin() as con: #inicializo a transação
            sql = """INSERT INTO public.itens_compras
                    (pedido_id, produto_id, quantidade, preco_unitario)
	                VALUES (:pedido_id, :produto_id, :quantidade, :preco_unitario)""";                   
            
            dados = {
                "pedido_id": itens_compra.pedido_id,
                "produto_id": itens_compra.produto_id,
                "quantidade": itens_compra.quantidade,
                "preco_unitario": itens_compra.preco_unitario
            }

            con.execute(text(sql), dados)

            return {"mensagem": "Item de compra cadastrado com sucesso"}

           
    except Exception as e:
        print(e)
        return {"erro": str(e), "detalhe": "Verifique os atributos da classe Itens_Compras"}
        

#recovery =>consulta (getOne e getAll => pegar 1 ou pegar todos)
@router.get("/{pedido_id}")
def getOne(pedido_id: int):

    try:
        with engine.begin() as con:
            sql = """
                SELECT 
                    p.cliente_id,
                    i.quantidade,
                    i.preco_unitario
                FROM public.pedidos p
                JOIN public.itens_compras i 
                    ON i.pedido_id = p.id
                WHERE p.id = :pedido_id
            """

            result = con.execute(
                text(sql),
                {"pedido_id": pedido_id}
            ).fetchall()

            if not result:
                return {"erro": "Pedido não encontrado"}

            return [dict(row._mapping) for row in result]

    except Exception as e:
        return {"erro": str(e)}
        

#postman http://localhost/cliente/todos
@router.get('/')
def todos():

    try:
        with engine.begin() as con:

            sql = """
                SELECT pedido_id, produto_id, quantidade, preco_unitario
	            FROM public.itens_compras
                ORDER BY  pedido_id, produto_id
            """

            result = con.execute(text(sql))

            itens_compras = [dict(row._mapping) for row in result]

        return itens_compras

    except Exception as e:
        return {"erro": str(e)}
    


@router.put('/{pedido_id}/{produto_id}')
def atualizar(pedido_id: int, produto_id: int, itens_compra: Itens_Compras):

#logica do update
    try:
        with engine.begin() as con:

            sql = """
                UPDATE public.itens_compras
	            SET pedido_id=:pedido_id, produto_id=:produto_id, quantidade=:quantidade, preco_unitario=:preco_unitario    

	            WHERE pedido_id = :pedido_id
                AND produto_id = :produto_id
            """

            dados = {
                    "pedido_id": pedido_id,
                     "produto_id": produto_id,
                    "quantidade": itens_compra.quantidade,
                 "preco_unitario": itens_compra.preco_unitario
                }

            result = con.execute(text(sql), dados)

            return {"mensagem": "Item de compra atualizado com sucesso"}

    except Exception as e:
        return {"erro": str(e)}

@router.delete("/{pedido_id}")
def deletar(pedido_id: int):
    
    try:
        with engine.begin() as con:
            sql = """
                DELETE FROM public.itens_compras
                WHERE pedido_id = :pedido_id 
                
                
            """

            con.execute(text(sql), {
                "pedido_id": pedido_id,
                
            })

        return {
            "mensagem": "Item de compra deletado com sucesso",
            "pedido_id": pedido_id,
           
        }
    except Exception as e:
        return {"erro": str(e)}
    
    
