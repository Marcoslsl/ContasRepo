from datetime import datetime, timedelta
from jose import jwt
import json

# CONFIGS
SECRET_KEY = "caa9c8f8620cbb30679026bb6427e11f"
ALGORITHM = "HS256"
EXPIRES_IN_MIN = 3000


def criar_access_token(data: dict) -> dict:
    """Create access token.

    Parameters
    ----------
    data: dict
        Carga de dados que vai ser armazenada no token.
    """
    expiracao = datetime.utcnow() + timedelta(minutes=EXPIRES_IN_MIN)
    data.update({"exp": expiracao})

    token_jwt = jwt.encode(data, key=SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt


def verificar_access_token(token: str) -> dict:
    """Check access token."""
    carga_de_dados = jwt.decode(
        str(token), key=SECRET_KEY, algorithms=[ALGORITHM]
    )
    r = {"pwd": carga_de_dados["sub_pwd"], "user": carga_de_dados["sub_user"]}
    return r
