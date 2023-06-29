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


def test_criar_fornecedor_cliente():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    response = client.post("/fornecedor-cliente", json={"name": "TEST"})
    assert response.status_code == 201


def test_listar_fornecedor_cliente():
    response = client.get("/fornecedor-cliente")
    assert response.status_code == 200


def test_get_by_id():
    client.post("/fornecedor-cliente/100", json={"name": "TEST"})
    response = client.get("/fornecedor-cliente/1")
    assert response.status_code == 200
    assert response.json()["name"] == "TEST"


def test_error_get_by_id():
    response = client.get("/fornecedor-cliente/100")
    assert response.status_code == 404
