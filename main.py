from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes_cliente import router as cliente_router
from routes_entregador import router as entregador_router
from routes_restaurante import router as restaurante_router
from routes_pedido import router as pedido_router
from routes_auth import router as auth_router
from database import engine
from models.base import Base
# Importa models necessários para criar as tabelas
from models.usuario import Usuario
from models.cliente import Cliente
from models.entregador import Entregador
from models.restaurante import Restaurante
from models.pedido import Pedido
from models.produto import Produto
from models.favorito import Favorito
from models.selos_cliente import SelosCliente
from models.restaurante_aluno import RestauranteAluno
from models.selos_produto import SelosProduto
from models.pedido_produto import PedidoProduto

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

# Cria as tabelas no banco de dados, se não existirem
Base.metadata.create_all(bind=engine)

print("Servidor iniciado com sucesso!")
