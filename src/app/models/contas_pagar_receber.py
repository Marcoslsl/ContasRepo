from decimal import Decimal
from pydantic import BaseModel


class ContaPagarReceberResponse(BaseModel):
    """Contas a pagar e receber."""

    id: int
    description: str
    valor: Decimal
    tipo: str

    class Config:
        """Configs."""

        orm_mode = True


class ContaPagarReceberRequest(BaseModel):
    """Contas a pagar e receber."""

    description: str
    valor: Decimal
    tipo: str
