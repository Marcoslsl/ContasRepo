from itertools import groupby
from datetime import date
from typing import List
from sqlalchemy import extract
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from src.app.erros.exceptions import NotFound
from src.infra.configs.dependencies import get_db
from src.infra.entities.conta_pagar_receber import ContasPagarReceber
from src.infra.entities.fornecedor_cliente import FornecedorCliente
from src.app.models.contas_pagar_receber import (
    ContaPagarReceberRequest,
    ContaPagarReceberResponse,
    ContasPagarRerecerTipo,
    PrevisaoPorMes,
)
from .auth.auth_utils import obter_usuario_logado

router = APIRouter(prefix="/contas-a-pagar-e-receber")

QUANTIDADE_PERMITIDA_POR_MES = 100


@router.get("/previsao-gastos-do-mes", response_model=List[PrevisaoPorMes])
def prev(db: Session = Depends(get_db), ano=date.today().year):
    """Previsao por mes."""
    return relatorio_gastos_previstos_por_mes_de_um_ano(db, ano)


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
) -> ContaPagarReceberResponse:
    """Listar conta."""
    conta = busca_conta_por_id(id_conta, db)
    return conta


@router.post("", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(
    conta: ContaPagarReceberRequest, db: Session = Depends(get_db)
) -> ContaPagarReceberResponse:
    """Criar conta."""
    validate_fornecedor(conta.fornecedor_cliente_id, db)
    excecao_quando_ultrapassa_numero_registros(conta, db)

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
    validate_fornecedor(conta.fornecedor_cliente_id, db)
    conta_pagar_receber = busca_conta_por_id(id_conta, db)
    conta_pagar_receber.tipo = conta.tipo
    conta_pagar_receber.valor = conta.valor
    conta_pagar_receber.description = conta.description

    db.add(conta_pagar_receber)
    db.commit()
    db.refresh(conta_pagar_receber)
    return conta_pagar_receber


@router.post(
    "/{id_conta}/baixar",
    response_model=ContaPagarReceberResponse,
    status_code=200,
)
def baixar_conta(
    id_conta: int,
    db: Session = Depends(get_db),
) -> ContaPagarReceberResponse:
    """Update."""
    conta_pagar_receber = busca_conta_por_id(id_conta, db)

    if (
        conta_pagar_receber.esta_baixada
        and conta_pagar_receber.valor == conta_pagar_receber.valor_baixa
    ):
        return conta_pagar_receber

    conta_pagar_receber.data_baixa = date.today()
    conta_pagar_receber.esta_baixada = True
    conta_pagar_receber.valor_baixa = conta_pagar_receber.valor

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


def busca_conta_por_id(id_conta: int, db: Session) -> ContasPagarReceber:
    """Get count by id."""
    conta = db.get(ContasPagarReceber, id_conta)
    if conta is None:
        raise NotFound("conta a pagar e receber")
    return conta


def validate_fornecedor(id: int | None, db: Session) -> None:
    """Validate fornecedor."""
    if id is not None:
        fornecedor = db.get(FornecedorCliente, id)
        if fornecedor is None:
            raise NotFound("Fornecedor")


def validate_numero_de_registros(db: Session, ano: int, mes: int):
    """Validate number of registries."""
    qtd_registros = (
        db.query(ContasPagarReceber)
        .filter(extract("year", ContasPagarReceber.data_previsao) == ano)
        .filter(extract("month", ContasPagarReceber.data_previsao) == mes)
        .count()
    )

    return qtd_registros


def excecao_quando_ultrapassa_numero_registros(
    conta: ContaPagarReceberRequest, db: Session
) -> None:
    """Raise exception when number of registries is higher than expected."""
    if (
        validate_numero_de_registros(
            db, conta.data_previsao.year, conta.data_previsao.month
        )
        >= QUANTIDADE_PERMITIDA_POR_MES
    ):
        raise HTTPException(
            status_code=422, detail="nao pode mais lancar conta esse mes."
        )


def relatorio_gastos_previstos_por_mes_de_um_ano(
    db: Session, ano: int
) -> List[PrevisaoPorMes]:
    """Get registries per month of year."""
    contas_do_ano = (
        db.query(ContasPagarReceber)
        .filter(extract("year", ContasPagarReceber.data_previsao) == ano)
        .filter(ContasPagarReceber.tipo == ContasPagarRerecerTipo.PAGAR)
        .all()
    )

    valor_por_mes = {}
    for conta in contas_do_ano:
        mes = conta.data_previsao.month

        if valor_por_mes.get(mes) is None:
            valor_por_mes[mes] = 0

        valor_por_mes[mes] += conta.valor

    conta_mes = [
        PrevisaoPorMes(mes=k, valor_total=v) for k, v in valor_por_mes.items()
    ]
    return sorted(conta_mes, key=lambda x: x.mes)
