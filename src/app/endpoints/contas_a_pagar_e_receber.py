from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from src.infra.configs.dependencies import get_db
from src.infra.entities.conta_pagar_receber import ContasPagarReceber
from src.app.models.contas_pagar_receber import (
    ContaPagarReceberRequest,
    ContaPagarReceberResponse,
)

router = APIRouter(prefix="/contas-a-pagar-e-receber")


@router.get("", response_model=List[ContaPagarReceberResponse])
def listar_contas(
    db: Session = Depends(get_db),
) -> List[ContaPagarReceberResponse]:
    """Listar contas."""
    return db.query(ContasPagarReceber).all()


@router.get("/{id_conta}", response_model=ContaPagarReceberResponse)
def get_unique_conta(
    id_conta: int,
    db: Session = Depends(get_db),
) -> List[ContaPagarReceberResponse]:
    """Listar conta."""
    conta = db.query(ContasPagarReceber).get(id_conta)
    return conta


@router.post("", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(
    conta: ContaPagarReceberRequest, db: Session = Depends(get_db)
) -> ContaPagarReceberResponse:
    """Criar conta."""
    contas = ContasPagarReceber(**conta.dict())
    db.add(contas)
    db.commit()
    db.refresh(contas)

    return contas


@router.put(
    "/{id_conta}", response_model=ContaPagarReceberResponse, status_code=200
)
def update_conta(
    id_conta: int,
    conta: ContaPagarReceberRequest,
    db: Session = Depends(get_db),
) -> ContaPagarReceberResponse:
    """Update."""
    conta_pagar_receber = db.query(ContasPagarReceber).get(id_conta)
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
    conta = db.query(ContasPagarReceber).get(id_conta)
    db.delete(conta)
    db.commit()
