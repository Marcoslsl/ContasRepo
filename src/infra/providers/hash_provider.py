from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


def gerar_hash(text: str) -> str:
    """Generate hash."""
    return pwd_context.hash(text)


def verificar_hash(text, hash) -> bool:
    """Verify hash."""
    return pwd_context.verify(text, hash)
