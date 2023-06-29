import random
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


def test_criar_conta():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    nova_conta = {
        "description": "test",
        "valor": 10,
        "tipo": "PAGAR",
        "data_previsao": "2022-11-29",
    }
    response = client.post("/contas-a-pagar-e-receber", json=nova_conta)
    assert response.status_code == 201
    assert "id" in response.json().keys()


def test_listar_contas():
    response = client.get("/contas-a-pagar-e-receber")
    assert response.status_code == 200
    assert isinstance(response.json(), List)


def test_listar_conta_unica():
    response = client.get("/contas-a-pagar-e-receber/1")
    assert response.status_code == 200


def test_delete_conta():
    id = 1
    response = client.delete(f"/contas-a-pagar-e-receber/{id}")
    assert response.status_code == 204


def test_update_conta():
    response = client.post(
        "/contas-a-pagar-e-receber",
        json={
            "description": "Curso de Python",
            "valor": 333,
            "tipo": "PAGAR",
            "data_previsao": "2022-11-29",
        },
    )

    id_da_conta_a_pagar_e_receber = response.json()["id"]

    response_put = client.put(
        f"/contas-a-pagar-e-receber/{id_da_conta_a_pagar_e_receber}",
        json={
            "description": "Curso de Python",
            "valor": 111,
            "tipo": "PAGAR",
            "data_previsao": "2022-11-29",
        },
    )

    assert response_put.status_code == 200
    assert response_put.json()["valor"] == 111


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


def test_return_not_found():
    response = client.get("/contas-a-pagar-e-receber/100")
    assert response.status_code == 404


def test_baixar_conta():
    nova_conta = {
        "description": "test",
        "valor": 10,
        "tipo": "PAGAR",
        "data_previsao": "2022-11-29",
    }
    r = client.post("/contas-a-pagar-e-receber", json=nova_conta)
    id = r.json()["id"]

    response = client.post(f"/contas-a-pagar-e-receber/{id}/baixar")
    assert response.status_code == 200
    assert response.json()["esta_baixada"] is True


def test_limite_de_registros_mensais():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    response = []
    for i in range(0, 101):
        r = client.post(
            "/contas-a-pagar-e-receber",
            json={
                "description": "TESTE",
                "valor": 100.0,
                "tipo": "PAGAR",
                "data_previsao": "2022-11-29",
            },
        )
        response.append(r.status_code)
    assert response[-1] == 422
    assert all([status == 201 for status in response[:-1]]) is True


def test_previsao_vazia():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    response = client.get("/contas-a-pagar-e-receber/previsao-gastos-do-mes")

    assert response.status_code == 200
    assert len(response.json()) == 0


def test_previsao():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    for i in range(0, 40):
        valor = 10
        mes = random.randint(1, 12)
        ano = 2022
        dia = 5

        client.post(
            "/contas-a-pagar-e-receber",
            json={
                "description": "TESTE",
                "valor": valor,
                "tipo": "PAGAR",
                "data_previsao": f"{ano}-{mes}-{dia}",
            },
        )

    response = client.get(
        f"/contas-a-pagar-e-receber/previsao-gastos-do-mes?ano={ano}"
    )

    total = []
    meses = []
    for i in response.json():
        total.append(i["valor_total"])
        meses.append(i["mes"])

    assert response.status_code == 200
    assert sum(total) == 400
    assert all(meses[i] <= meses[i + 1] for i in range(len(meses) - 1))
