import os

# 1. Tenta ler do Render. Se não achar, usa a sua string local como plano de fundo.
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # O Render envia 'postgres://', mas o SQLAlchemy moderno exige 'postgresql://'
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
else:
    # Se você estiver rodando local e não tiver a variável de ambiente configurada
    DATABASE_URL = "postgresql://YwMgiALSK8ksLyWc8fq6XF9qQGArHurh@dpg-d8uiffbeo5us73dvqdi0-a.oregon-postgres.render.com/banco_c99m"