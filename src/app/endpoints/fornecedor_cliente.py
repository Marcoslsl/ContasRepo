from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from src.app.erros.exceptions import NotFound
from src.infra.configs.dependencies import get_db
from src.infra.entities.fornecedor_cliente import FornecedorCliente
from src.app.models.fornecedor_cliente import (
    FornecedorClienteRequest,
    FornecedorClienteResponse,
)

router = APIRouter(prefix="/fornecedor-cliente")


@router.get("", response_model=List[FornecedorClienteResponse])
def listar_contas(
    db: Session = Depends(get_db),
) -> List[FornecedorClienteResponse]:
    """Listar contas."""
    return db.query(FornecedorCliente).all()


@router.get("/{id_conta}", response_model=FornecedorClienteResponse)
def get_unique_conta(
    id_conta: int,
    db: Session = Depends(get_db),
) -> FornecedorClienteResponse:
    """Listar conta."""
    conta = busca_conta_por_id(id_conta, db)
    return conta


@router.post("", response_model=FornecedorClienteResponse, status_code=201)
def criar_conta(
    conta: FornecedorClienteRequest, db: Session = Depends(get_db)
) -> FornecedorClienteResponse:
    """Criar conta."""
    contas = FornecedorCliente(**conta.dict())
    db.add(contas)
    db.commit()
    db.refresh(contas)

    return contas


@router.put(
    "/{id_conta}", response_model=FornecedorClienteResponse, status_code=200
)
def update_conta(
    id_conta: int,
    conta: FornecedorClienteRequest,
    db: Session = Depends(get_db),
) -> FornecedorClienteResponse:
    """Update."""
    conta_pagar_receber = busca_conta_por_id(id_conta, db)
    conta_pagar_receber.tipo = conta.tipo
    conta_pagar_receber.valor = conta.valor
    conta_pagar_receber.description = conta.description

    db.add(conta_pagar_receber)
    db.commit()
    db.refresh(conta_pagar_receber)
    return conta_pagar_receber


@router.delete("/{id_conta}", status_code=204)
def delete_conta(id_conta: int, db: Session = Depends(get_db)) -> None:
    """Delete."""
    conta = busca_conta_por_id(id_conta, db)
    db.delete(conta)
    db.commit()


def busca_conta_por_id(id_conta: int, db: Session) -> FornecedorCliente:
    """Get count by id."""
    conta = db.get(FornecedorCliente, id_conta)
    if conta is None:
        raise NotFound("conta a pagar e receber")
    return conta
