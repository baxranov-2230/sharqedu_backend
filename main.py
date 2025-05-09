from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api import main_router
import uvicorn

app = FastAPI(
    # docs_url=None,  # Swagger UI ni o'chirish
    # redoc_url=None  # ReDoc ni o'chirish
)

app.include_router(main_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=[
        "https://sharqedu.uz",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ],
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
