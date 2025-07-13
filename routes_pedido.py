from fastapi import APIRouter, HTTPException
from schemas.pedido import PedidoRead, PedidoCreate, PedidoBase
from typing import List
from datetime import datetime

router = APIRouter()

# Mock data para exemplo
db_pedidos = [
    {
        "pedido_id": 1,
        "cliente_id": 1,
        "restaurante_id": 1,
        "entregador_id": 1,
        "status": "em preparo",
        "preco_total": 80.00,
        "localizacao": "Rua das Flores, 123",
        "data_hora": datetime.now(),
        "observacao": "Sem cebola"
    },
    {
        "pedido_id": 2,
        "cliente_id": 1,
        "restaurante_id": 2,
        "entregador_id": None,
        "status": "aguardando",
        "preco_total": 45.00,
        "localizacao": "Av. Central, 456",
        "data_hora": datetime.now(),
        "observacao": None
    }
]

# Endpoints de Pedido
@router.get("/pedidos/{id}", response_model=PedidoRead)
def acompanhar_pedido(id: int):
    for p in db_pedidos:
        if p["pedido_id"] == id:
            return p
    raise HTTPException(status_code=404, detail="Pedido não encontrado")

@router.get("/pedidos/historico/{usuario_id}", response_model=List[PedidoRead])
def historico_pedidos(usuario_id: int):
    historico = [p for p in db_pedidos if p["cliente_id"] == usuario_id]
    return historico

@router.post("/pedidos", response_model=PedidoRead)
def criar_pedido(pedido: PedidoBase):
    novo_id = len(db_pedidos) + 1
    novo_pedido = pedido.model_dump()
    novo_pedido.update({"pedido_id": novo_id, "data_hora": datetime.now()})
    db_pedidos.append(novo_pedido)
    return novo_pedido

@router.put("/pedidos/{id}/status")
def atualizar_status_pedido(id: int, status: str):
    for p in db_pedidos:
        if p["pedido_id"] == id:
            p["status"] = status
            return {"pedido_id": id, "novo_status": status}
    raise HTTPException(status_code=404, detail="Pedido não encontrado")

@router.put("/pedidos/{id}/cancelar")
def cancelar_pedido(id: int):
    for p in db_pedidos:
        if p["pedido_id"] == id:
            p["status"] = "cancelado"
            return {"pedido_id": id, "novo_status": "cancelado"}
    raise HTTPException(status_code=404, detail="Pedido não encontrado")
