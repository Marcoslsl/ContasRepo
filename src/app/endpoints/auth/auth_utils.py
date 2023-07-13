from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends
from src.infra.configs.dependencies import get_db
from fastapi import HTTPException
from src.infra.providers.token_provider import verificar_access_token
from src.infra.repository.user_repo import UserRepo
from src.app.models.user_auth import User
from src.infra.providers.token_provider import criar_access_token


oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


def obter_usuario_logado(
    token: str = Depends(oauth2_schema), Session: Session = Depends(get_db)
) -> User:
    """Get user logged."""
    try:
        sub_dict = verificar_access_token(token=token)
        pwd = sub_dict["pwd"]
        name = sub_dict["user"]
    except Exception as e:
        # TO DO LOG
        raise HTTPException(status_code=401, detail="Invalid Token")

    if not pwd:
        print("exp 2")
        raise HTTPException(status_code=401, detail="Invalid Token")

    try:
        usuario = UserRepo(Session).get(name)[0]
    except Exception as e:
        raise HTTPException(status_code=401, detail="User token Error")

    return User(user=usuario.user, pwd=usuario.pwd)
