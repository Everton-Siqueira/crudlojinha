from fastapi import APIRouter
from itens_compras import ItemCompra


#pip install sqlalchemy
from sqlalchemy import create_engine, text
router = APIRouter(prefix="/itens_compras", tags=["Itens de Compras"])


#inserção no banco "postgresql://usuario:senha@servidor:porta/banco"
DATABASE_URL = "postgresql://postgres:123@localhost:5432/crudlojinha"


#REST
#Create
@router.post('/')
def cadastrar(item_compra: ItemCompra):

    #crio a conexao
    engine = create_engine(DATABASE_URL)


    try:
        with engine.begin() as con: #inicializo a transação
            sql = """INSERT INTO public.itens_compras
                    (pedido_id, produto_id, quantidade, preco_unitario)
	                VALUES (:pedido_id, :produto_id, :quantidade, :preco_unitario)""";                   
            
            dados = {
                "pedido_id": item_compra.pedido_id,
                "produto_id": item_compra.produto_id,
                "quantidade": item_compra.quantidade,
                "preco_unitario": item_compra.preco_unitario
            }

            con.execute(text(sql), dados)

            return {"mensagem": "Item de compra cadastrado com sucesso"}

           
    except Exception as e:
        print(e)
    engine.dispose()
        

#recovery =>consulta (getOne e getAll => pegar 1 ou pegar todos)
@router.get("/{pedido_id}/{produto_id}")
def getOne(pedido_id: int, produto_id: int):
    engine = create_engine(DATABASE_URL)

    with engine.begin() as con:
        sql = """
            SELECT pedido_id, produto_id, quantidade, preco_unitario
            FROM public.itens_compras
            WHERE pedido_id = :pedido_id
              AND produto_id = :produto_id
        """

        result = con.execute(
            text(sql),
            {
                "pedido_id": pedido_id,
                "produto_id": produto_id
            }
        ).fetchone()

        if result is None:
            return {"erro": "Item não encontrado"}

        return dict(result._mapping)

#postman http://localhost/cliente/todos
@router.get('/')
def todos():
    engine = create_engine(DATABASE_URL)

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
def atualizar(pedido_id: int, produto_id: int, item_compra: ItemCompra):


    engine = create_engine(DATABASE_URL)
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
                    "quantidade": item_compra.quantidade,
                 "preco_unitario": item_compra.preco_unitario
                }

            result = con.execute(text(sql), dados)

            return {"mensagem": "Item de compra atualizado com sucesso"}

    except Exception as e:
        return {"erro": str(e)}
    
    

@router.delete("/{pedido_id}/{produto_id}")
def deletar(pedido_id: int, produto_id: int):
    engine = create_engine(DATABASE_URL)

    try:
        with engine.begin() as con:
            sql = """
                DELETE FROM public.itens_compras
                WHERE pedido_id = :pedido_id 
                AND produto_id = :produto_id
                
            """

            con.execute(text(sql), {
                "pedido_id": pedido_id,
                "produto_id": produto_id
            })

        return {
            "mensagem": "Item de compra deletado com sucesso",
            "pedido_id": pedido_id,
            "produto_id": produto_id
        }
    except Exception as e:
        return {"erro": str(e)}
    
