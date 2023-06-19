import uvicorn
from fastapi import FastAPI
from src.app.routes import router
from src.infra.configs.database import engine
from src.infra.configs.base import Base
from src.infra.entities.conta_pagar_receber import ContasPagarReceber

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)


@app.get("/")
def main() -> str:
    """Test main func."""
    return "hello world"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
