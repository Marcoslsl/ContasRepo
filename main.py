import uvicorn
from fastapi import FastAPI, Request, BackgroundTasks
from src.app.routes import router
from src.infra.configs.database import engine
from src.infra.configs.base import Base
from src.infra.entities.conta_pagar_receber import ContasPagarReceber
from src.app.erros.exceptions import *
from src.job.write_notification import write_notification

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
app.add_exception_handler(NotFound, not_found_exception_handler)
app.add_exception_handler(BadRequest, bad_request_exception_handler)


# Middleware
@app.middleware("http")
async def processar_tempo_requisicao(request: Request, next):
    """Middleware teste."""
    print("interceptou...")
    response = await next(request)
    print("interceptou a volta...")
    return response


# Backgroundtask - works as a rabbitMq
@app.post("/send-email/{email}")
def send_email(email: str, background: BackgroundTasks):
    """Background task."""
    background.add_task(write_notification, email, "menssagem teste")
    return {"OK": "menssagem enviada"}


@app.get("/")
def home() -> str:
    """Test main func."""
    return "home"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
