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
testingSessionLocal = sessionmaker(autocommit=False, bind=engine)


def override_get_db():
    db = testingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_criar_conta():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    nova_conta = {"description": "test", "valor": 10, "tipo": "PAGAR"}
    response = client.post("/contas-a-pagar-e-receber", json=nova_conta)
    assert response.status_code == 201
    assert "id" in response.json().keys()


def test_listar_contas():
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
    response = client.get("/contas-a-pagar-e-receber")
    assert response.status_code == 200
    assert isinstance(response.json(), List)


def test_listar_conta_unica():
    response = client.get("/contas-a-pagar-e-receber/1")
    assert response.status_code == 200


def test_update_conta():
    # nova_conta = {"description": "test", "valor": 10, "tipo": "PAGAR"}
    # response = client.post("/contas-a-pagar-e-receber", json=nova_conta)
    # id = response.json()['id']
    id = 1
    nova_conta = {"description": "testUpdate", "valor": 10, "tipo": "PAGAR"}
    response = client.put(f"/contas-a-pagar-e-receber/{id}", json=nova_conta)
    assert response.status_code == 200
    assert response.json()["description"] == "testUpdate"


def test_delete_conta():
    id = 1
    response = client.delete(f"/contas-a-pagar-e-receber/{id}")
    assert response.status_code == 204


def test_return_error_description():
    data = {
        "description": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "valor": 333,
        "tipo": "RECEBER",
    }
    response = client.post("/contas-a-pagar-e-receber", json=data)
    assert response.status_code == 422


def test_return_error_valor():
    data = {"description": "description", "valor": -1, "tipo": "RECEBER"}
    response = client.post("/contas-a-pagar-e-receber", json=data)
    assert response.status_code == 422


def test_return_error_tipo():
    data = {"description": "description", "valor": 1, "tipo": "test"}
    response = client.post("/contas-a-pagar-e-receber", json=data)
    assert response.status_code == 422
