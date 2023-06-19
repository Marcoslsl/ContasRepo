from sqlalchemy import Column, Integer, String, Numeric
from src.infra.configs.base import Base


class ContasPagarReceber(Base):
    """Contas pagar receber."""

    __tablename__ = "contas_a_pagar_e_receber"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(36))
    valor = Column(Numeric)
    tipo = Column(String(30))
