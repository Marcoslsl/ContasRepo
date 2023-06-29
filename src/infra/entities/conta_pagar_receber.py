from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Date,
    ForeignKey,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship
from src.infra.configs.base import Base
from datetime import date


class ContasPagarReceber(Base):
    """Contas pagar receber."""

    __tablename__ = "contas_a_pagar_e_receber"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(36))
    valor = Column(Numeric)
    tipo = Column(String(30))
    data_previsao = Column(Date(), default=date.today())
    data_baixa = Column(DateTime())
    valor_baixa = Column(Numeric())
    esta_baixada = Column(Boolean, default=False)

    fornecedor_cliente_id = Column(
        Integer, ForeignKey("fornecedor_cliente.id")
    )
    fornecedor = relationship("FornecedorCliente")
