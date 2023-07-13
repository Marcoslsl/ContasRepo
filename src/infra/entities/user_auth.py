from sqlalchemy import Column, Integer, String
from src.infra.configs.base import Base


class UserAuth(Base):
    """User Auth."""

    __tablename__ = "user_auth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(255))
    pwd = Column(String(255))
