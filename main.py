

from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.api import main_router
import uvicorn
ALLOWED_IP = "213.230.124.102"

app = FastAPI(
    # docs_url=None,  # Swagger UI ni o'chirish
    # redoc_url=None  # ReDoc ni o'chirish
)

@app.get("/real-ip")
async def get_real_ip(request: Request):
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        ip = forwarded_for.split(",")[0]
    else:
        ip = request.client.host
    return {"ip": ip}



class SwaggerAccessMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json"):
            client_ip = request.client.host
            if client_ip != ALLOWED_IP:
                raise HTTPException(status_code=403, detail="Swagger sahifasiga kirishga ruxsat yo'q")
        return await call_next(request)

app.add_middleware(SwaggerAccessMiddleware)



app.include_router(main_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=[
        "https://sharqedu.uz",
        "http://admin.sharqedu.uz",
        "https://admin.sharqedu.uz",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ],
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
