from decimal import Decimal
from pydantic import BaseModel, Field
from enum import Enum


class ContaPagarReceberResponse(BaseModel):
    """Contas a pagar e receber."""

    id: int
    description: str
    valor: Decimal
    tipo: str

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
