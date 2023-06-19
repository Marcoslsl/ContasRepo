from typing import List
from fastapi import APIRouter
from src.app.models.contas_pagar_receber import (
    ContaPagarReceberRequest,
    ContaPagarReceberResponse,
)

router = APIRouter(prefix="/contas-a-pagar-e-receber")


@router.get("/", response_model=List[ContaPagarReceberResponse])
def listar_contas():
    """Listar contas."""
    return [
        ContaPagarReceberResponse(
            id=1, description="alugel", valor=100.70, tipo="pagar"
        )
    ]


@router.post("/", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta: ContaPagarReceberRequest):
    """Criar conta."""
    return ContaPagarReceberResponse(
        id=3, description=conta.description, valor=conta.valor, tipo=conta.tipo
    )
