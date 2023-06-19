from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

host = "localhost"  # Endereço do servidor MySQL
port = "3306"  # Porta do servidor MySQL (padrão: 3306)
database = "pipeline_db"  # Nome do banco de dados
user = "root"  # Usuário do banco de dados
password = "1234"  # Senha do usuário do banco de dados

# Criando a string de conexão
connection_string = (
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
)

engine = create_engine(connection_string)
SessionLocal = sessionmaker(bind=engine)
