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
