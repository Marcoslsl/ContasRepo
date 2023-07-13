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
from src.app.models.user_auth import User, UserNoPwd, LoginSucess
from src.infra.repository.user_repo import UserRepo, UserAuth
from src.infra.providers.hash_provider import gerar_hash, verificar_hash
from src.infra.providers.token_provider import (
    criar_access_token,
    verificar_access_token,
)
from src.app.erros.exceptions import BadRequest
from .auth.auth_utils import obter_usuario_logado


router = APIRouter(prefix="/auth")


@router.post("/sign-up", status_code=201, response_model=UserNoPwd)
def signup(usuario: User, Session: Session = Depends(get_db)):
    """Signup."""
    repo = UserRepo(Session)

    user_found = repo.get(usuario.user)
    if len(user_found) != 0:
        raise BadRequest("User already exists")

    usuario.pwd = gerar_hash(usuario.pwd)
    usuario_criado = repo.create(usuario)
    return usuario_criado


@router.post("/token", status_code=200, response_model=LoginSucess)
def signin(usuario: User, Session: Session = Depends(get_db)):
    """Login."""
    repo = UserRepo(Session)

    user_found = repo.get(usuario.user)
    if len(user_found) == 0:
        raise NotFound("User")

    senha_valida = verificar_hash(usuario.pwd, user_found[0].pwd)
    if not senha_valida:
        raise BadRequest("Incorrect Password.")

    # Gerar token JWT
    token = criar_access_token(
        {"sub_pwd": usuario.pwd, "sub_user": usuario.user}
    )
    return LoginSucess(user=usuario.user, access_token=token)


@router.get("/me", status_code=200)
def me(usuario: User = Depends(obter_usuario_logado)):
    """Me."""
    return {"user": usuario.user, "details": "Usuario logado"}
