from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from src.app.erros.exceptions import NotFound
from src.infra.configs.dependencies import get_db
from src.infra.entities.fornecedor_cliente import FornecedorCliente
from src.infra.entities.conta_pagar_receber import ContasPagarReceber
from src.app.models.fornecedor_cliente import (
    FornecedorClienteRequest,
    FornecedorClienteResponse,
)
from src.app.models.contas_pagar_receber import ContaPagarReceberResponse

router = APIRouter(prefix="/fornecedor-cliente")


@router.get(
    "/{id_conta}/contas-a-pagar-e-receber",
    response_model=List[ContaPagarReceberResponse],
)
def get_unique_conta(
    id_conta: int,
    db: Session = Depends(get_db),
) -> List[ContaPagarReceberResponse]:
    """Listar conta."""
    response = (
        db.query(ContasPagarReceber)
        .filter_by(fornecedor_cliente_id=id_conta)
        .all()
    )
    return response
