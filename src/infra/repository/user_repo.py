from sqlalchemy.orm import Session
from src.app.models.user_auth import User, UserNoPwd
from src.infra.entities.user_auth import UserAuth
from src.infra.configs.database import engine


class UserRepo:
    """User repo."""

    def __init__(self, session: Session) -> None:
        """Construct."""
        self._session = session

    def create(self, conta: User):
        """Create."""
        user = UserAuth(**conta.dict())
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return UserNoPwd(user=conta.user)

    def get_user(self, user_name: str):
        """Get user by name."""
        user_found = (
            self._session.query(UserAuth)
            .filter(UserAuth.user == user_name)
            .all()
        )
        return user_found
