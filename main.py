from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes_cliente import router as cliente_router
from routes_entregador import router as entregador_router
from routes_restaurante import router as restaurante_router
from routes_pedido import router as pedido_router
from routes_auth import router as auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cliente_router)
app.include_router(entregador_router)
app.include_router(restaurante_router)
app.include_router(pedido_router)
app.include_router(auth_router)

