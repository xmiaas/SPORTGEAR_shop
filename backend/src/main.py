import uvicorn
from database import DATABASE_URL
from fastapi import FastAPI

from src.products.router import router as product_router
from src.auth.router import authRouter
app = FastAPI()

app.include_router(product_router)
app.include_router(authRouter)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

