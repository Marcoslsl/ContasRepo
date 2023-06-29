from typing import List
from fastapi.testclient import TestClient
from src.app.models.contas_pagar_receber import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infra.configs.dependencies import get_db
from src.infra.configs.base import Base
from main import app

client = TestClient(app)
SQLALCHEMY_DATABASE_URL = "sqlite:///./src/tests/test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_listar_contas_um_fornecedor():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    client.post("/fornecedor-cliente", json={"name": "TEST"})

    nova_conta = {
        "description": "test",
        "valor": 10,
        "tipo": "PAGAR",
        "fornecedor_cliente_id": 1,
        "data_previsao": "2022-11-29",
    }
    nova_conta_2 = {
        "description": "test_2",
        "valor": 10,
        "tipo": "PAGAR",
        "fornecedor_cliente_id": 1,
        "data_previsao": "2022-11-29",
    }
    client.post("/contas-a-pagar-e-receber", json=nova_conta)
    client.post("/contas-a-pagar-e-receber", json=nova_conta_2)

    response = client.get(f"/fornecedor-cliente/1/contas-a-pagar-e-receber")
    assert response.status_code == 200
    assert len(response.json()) == 2


# def test_return_lista_vazia()
