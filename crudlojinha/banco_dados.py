import os

# 1. Tenta ler a variável configurada no painel do Render
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Se o Render não encontrar a variável (ficar None ou vazia), força a URL direta
if not DATABASE_URL:
    DATABASE_URL = "postgresql://YwMgiALSK8ksLyWc8fq6XF9qQGArHurh@dpg-d8uiffbeo5us73dvqdi0-a.oregon-postgres.render.com/banco_c99m?sslmode=require"
else:
    # Correção extra para o Render que às vezes envia 'postgres://' em vez de 'postgresql://'
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        
    # Garante que o SSL está ativo na string vinda do Render
    if "?sslmode=" not in DATABASE_URL:
        DATABASE_URL += "?sslmode=require"