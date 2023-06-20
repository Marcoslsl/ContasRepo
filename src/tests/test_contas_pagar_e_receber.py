from typing import List
from fastapi.testclient import TestClient
from src.app.models.contas_pagar_receber import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infra.configs.dependencies import get_db
from main import app

client = TestClient(app)
SQLALCHEMY_DATABASE_URL = "sqlite:///./src/tests/test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
testingSessionLocal = sessionmaker(autocommit=False, bind=engine)


def override_get_db():
    db = testingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_listar_contas():
    response = client.get("/contas-a-pagar-e-receber")
    assert response.status_code == 200
    assert isinstance(response.json(), List)


def test_criar_conta():
    nova_conta = {"description": "test", "valor": 10, "tipo": "test"}
    response = client.post("/contas-a-pagar-e-receber", json=nova_conta)
    assert response.status_code == 201
    assert "id" in response.json().keys()
