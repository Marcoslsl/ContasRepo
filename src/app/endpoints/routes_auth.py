from fastapi import APIRouter
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from src.app.erros.exceptions import NotFound
from src.infra.configs.dependencies import get_db
from src.infra.entities.fornecedor_cliente import FornecedorCliente
from src.app.models.fornecedor_cliente import (
    FornecedorClienteRequest,
    FornecedorClienteResponse,
)
from src.app.models.user_auth import User, UserNoPwd
from src.infra.repository.user_repo import UserRepo, UserAuth
from src.infra.providers.hash_provider import gerar_hash
from src.app.erros.exceptions import BadRequest


router = APIRouter(prefix="/auth")


@router.post("/signup", status_code=201, response_model=UserNoPwd)
def signup(usuario: User, Session: Session = Depends(get_db)):
    """Signup."""
    repo = UserRepo(Session)

    user_found = repo.get(usuario.user)
    if len(user_found) != 0:
        raise BadRequest("User already exists")

    usuario.pwd = gerar_hash(usuario.pwd)
    usuario_criado = repo.create(usuario)
    return usuario_criado
