from .fornecedor_cliente import FornecedorClienteResponse
from decimal import Decimal
from pydantic import BaseModel, Field
from enum import Enum
from datetime import date


class PrevisaoPorMes(BaseModel):
    """Previsao por mes."""

    mes: int
    valor_total: Decimal


class ContaPagarReceberResponse(BaseModel):
    """Contas a pagar e receber."""

    id: int
    description: str
    valor: Decimal
    tipo: str
    data_previsao: date
    data_baixa: date | None
    valor_baixa: Decimal | None
    esta_baixada: bool | None
    fornecedor: FornecedorClienteResponse | None

    class Config:
        """Configs."""

        orm_mode = True


class ContasPagarRerecerTipo(str, Enum):
    """Tipo."""

    PAGAR = "PAGAR"
    RECEBER = "RECEBER"


class ContaPagarReceberRequest(BaseModel):
    """Contas a pagar e receber."""

    description: str = Field(min_length=3, max_length=30)
    valor: Decimal = Field(gt=0)
    tipo: ContasPagarRerecerTipo
    fornecedor_cliente_id: int | None = None
    data_previsao: date
