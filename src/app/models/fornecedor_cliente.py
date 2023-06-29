from pydantic import BaseModel, Field


class FornecedorClienteResponse(BaseModel):
    """Fornecedor Cliente."""

    id: int
    name: str

    class Config:
        """Configs."""

        orm_mode = True


class FornecedorClienteRequest(BaseModel):
    """Fornecedor Cliente."""

    name: str = Field(min_length=3, max_length=255)
