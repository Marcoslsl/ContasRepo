from fastapi.responses import JSONResponse
from fastapi import Request


class NotFound(Exception):
    """Not Found."""

    def __init__(self, name: str):
        """Construct."""
        self.name = name


async def not_found_exception_handler(request: Request, exc: NotFound):
    """Not found."""
    return JSONResponse(
        status_code=404, content={"message": f"Oops! {exc.name} not found."}
    )
