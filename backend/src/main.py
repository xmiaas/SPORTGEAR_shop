import uvicorn
from database import DATABASE_URL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.products.router import router as product_router
from src.auth.router import authRouter
from src.orders.router import basketRouter
from src.admin.router import adminRouter

app = FastAPI()

app.include_router(product_router)
app.include_router(authRouter)
app.include_router(basketRouter)
app.include_router(adminRouter)

origins = ["http://127.0.0.1:5500"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Разрешает запросы от указанных источников (можно использовать ["*"] для всех)
    allow_credentials=True,       # Разрешает передачу кук и авторизационных заголовков (Authorization)
    allow_methods=["*"],          # Разрешает все HTTP-методы (GET, POST, PUT и др.)
    allow_headers=["*"],          # Разрешает все HTTP-заголовки
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

