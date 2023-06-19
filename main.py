import uvicorn
from fastapi import FastAPI
from src.app.routes import router

app = FastAPI()
app.include_router(router)


@app.get("/")
def main() -> str:
    """Test main func."""
    return "hello world"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
