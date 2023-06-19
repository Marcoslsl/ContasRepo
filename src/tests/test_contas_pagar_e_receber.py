from typing import List
from fastapi.testclient import TestClient
from src.app.models.contas_pagar_receber import *
from main import app

client = TestClient(app)


def test_listar_contas():
    response = client.get("/contas-a-pagar-e-receber")
    assert response.status_code == 200
    assert isinstance(response.json(), List)


def test_criar_conta():
    nova_conta = {"description": "test", "valor": 10, "tipo": "test"}
    response = client.post("/contas-a-pagar-e-receber", json=nova_conta)
    assert response.status_code == 201
    assert "id" in response.json().keys()
