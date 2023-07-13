from abc import abstractmethod, ABC


class RepoInterface(ABC):
    """Repository interface."""

    @abstractmethod
    def create():
        """Create."""
        raise NotImplementedError("Must be implemented")

    @abstractmethod
    def delete():
        """Delete."""
        raise NotImplementedError("Must be implemented")

    @abstractmethod
    def update():
        """Update."""
        raise NotImplementedError("Must be implemented")

    @abstractmethod
    def get():
        """Get."""
        raise NotImplementedError("Must be implemented")
