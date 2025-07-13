from fastapi import APIRouter, HTTPException
from schemas.usuario import UsuarioCreate, UsuarioRead
from typing import Dict
from routes_cliente import db_clientes
from routes_entregador import db_entregadores
from routes_restaurante import db_restaurantes
from pydantic import BaseModel, EmailStr

router = APIRouter()

# Mock banco de usuários
mock_usuarios = [
    {"usuario_id": 1, "nome": "Cliente Teste", "email": "cliente@email.com", "senha": "123", "papel": "cliente"},
    {"usuario_id": 2, "nome": "Entregador Teste", "email": "entregador@email.com", "senha": "123", "papel": "entregador"},
    {"usuario_id": 3, "nome": "Restaurante Sabor Caseiro", "email": "saborcaseiro@email.com", "senha": "123", "papel": "restaurante"},
    {"usuario_id": 4, "nome": "Pizzaria Bella Massa", "email": "bellamassa@email.com", "senha": "123", "papel": "restaurante"}
]

class AuthRequest(BaseModel):
    email: EmailStr
    senha: str

def autenticar(email: str, senha: str, papel: str) -> Dict:
    for u in mock_usuarios:
        if u["email"] == email and u["senha"] == senha and u["papel"] == papel:
            return {"usuario_id": u["usuario_id"], "nome": u["nome"], "email": u["email"], "papel": papel}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

# Endpoints de Autenticação

@router.post("/auth/cliente", response_model=UsuarioRead)
def autenticar_cliente(auth: AuthRequest):
    return autenticar(str(auth.email), auth.senha, "cliente")

@router.post("/auth/entregador", response_model=UsuarioRead)
def autenticar_entregador(auth: AuthRequest):
    return autenticar(str(auth.email), auth.senha, "entregador")

@router.post("/auth/restaurante", response_model=UsuarioRead)
def autenticar_restaurante(auth: AuthRequest):
    return autenticar(str(auth.email), auth.senha, "restaurante")

@router.post("/auth/login")
def login(auth: AuthRequest):
    for u in mock_usuarios:
        if u["email"] == str(auth.email) and u["senha"] == auth.senha:
            return {"usuario_id": u["usuario_id"], "nome": u["nome"], "email": u["email"], "papel": u["papel"]}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

@router.post("/auth/registrar/cliente", response_model=UsuarioRead)
def registrar_cliente(usuario: UsuarioCreate):
    novo_id = len(mock_usuarios) + 1
    novo_usuario = {
        "usuario_id": novo_id,
        "nome": usuario.nome,
        "email": usuario.email,
        "senha": usuario.senha,
        "papel": "cliente"
    }
    mock_usuarios.append(novo_usuario)
    # Adiciona também ao db_clientes
    db_clientes.append({
        "cliente_id": novo_id,
        "usuario_id": novo_id,
        "saldo": 0.0})
    return {"usuario_id": novo_id, "nome": usuario.nome, "email": usuario.email}

@router.post("/auth/registrar/entregador", response_model=UsuarioRead)
def registrar_entregador(usuario: UsuarioCreate):
    novo_id = len(mock_usuarios) + 1
    novo_usuario = {
        "usuario_id": novo_id,
        "nome": usuario.nome,
        "email": usuario.email,
        "senha": usuario.senha,
        "papel": "entregador"
    }
    mock_usuarios.append(novo_usuario)
    # Adiciona também ao db_entregadores
    db_entregadores.append({
        "entregador_id": novo_id,
        "usuario_id": novo_id,
        "veiculo": "",
        "avaliacao": 0.0,
        "saldo": "0.00",
        "disponivel": False})
    return {"usuario_id": novo_id, "nome": usuario.nome, "email": usuario.email}

@router.post("/auth/registrar/restaurante", response_model=UsuarioRead)
def registrar_restaurante(usuario: UsuarioCreate):
    novo_id = len(mock_usuarios) + 1
    novo_usuario = {
        "usuario_id": novo_id,
        "nome": usuario.nome,
        "email": usuario.email,
        "senha": usuario.senha,
        "papel": "restaurante"
    }
    mock_usuarios.append(novo_usuario)
    # Adiciona também ao db_restaurantes
    db_restaurantes.append({
        "restaurante_id": novo_id,
        "usuario_id": novo_id,
        "nome": usuario.nome,
        "info": "Novo restaurante",
        "local": "",
        "email": usuario.email,
        "horario_abertura": "09:00",
        "horario_fechamento": "22:00",
        "numero_estrelas": 0.0,
        "disponivel": False,
        "telefone": "",
        "tipo_restaurante": "",
        "saldo": "0.00"
    })
    return {"usuario_id": novo_id, "nome": usuario.nome, "email": usuario.email}
