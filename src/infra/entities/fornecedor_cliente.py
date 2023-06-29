from sqlalchemy import Column, Integer, String
from src.infra.configs.base import Base


class FornecedorCliente(Base):
    """Fornecedor cliente."""

    __tablename__ = "fornecedor_cliente"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
