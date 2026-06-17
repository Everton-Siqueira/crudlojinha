from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:123@localhost:5432/lojinha"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    resultado = conn.execute(text("SELECT 1"))
    print(resultado.scalar())