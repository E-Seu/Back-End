from fastapi import APIRouter, HTTPException
from schemas.cliente import ClienteRead
from typing import List

router = APIRouter()

# Mock data para exemplo
db_clientes = [
    {"cliente_id": 1, "usuario_id": 1, "saldo": 200.00},
    {"cliente_id": 2, "usuario_id": 2, "saldo": 150.00}
]
db_favoritos = {
    1: [1, 2],  # cliente_id: [restaurante_ids]
    2: [2]
}
db_restricoes = {
    1: ["sem lactose"],
    2: []
}

# Endpoints de Cliente
@router.get("/clientes/{id}", response_model=ClienteRead)
def get_cliente(id: int):
    for c in db_clientes:
        if c["cliente_id"] == id:
            return c
    raise HTTPException(status_code=404, detail="Cliente não encontrado")

@router.get("/clientes/{id}/favorito")
def listar_favoritos(id: int):
    return {"cliente_id": id, "favoritos": db_favoritos.get(id, [])}

@router.get("/clientes/{id}/saldo")
def visualizar_saldo(id: int):
    for c in db_clientes:
        if c["cliente_id"] == id:
            return {"cliente_id": id, "saldo": c["saldo"]}
    raise HTTPException(status_code=404, detail="Cliente não encontrado")

@router.post("/clientes/{id}/favorito/{restaurante_id}")
def adicionar_favorito(id: int, restaurante_id: int):
    db_favoritos.setdefault(id, []).append(restaurante_id)
    return {"cliente_id": id, "favoritos": db_favoritos[id]}

@router.put("/clientes/{id}/restricoes")
def atualizar_restricoes(id: int, restricoes: List[str]):
    db_restricoes[id] = restricoes
    return {"cliente_id": id, "restricoes": restricoes}

@router.put("/clientes/{id}/saldo")
def atualizar_saldo(id: int, saldo: float):
    for c in db_clientes:
        if c["cliente_id"] == id:
            c["saldo"] = saldo
            return {"cliente_id": id, "saldo": saldo}
    raise HTTPException(status_code=404, detail="Cliente não encontrado")

@router.delete("/clientes/{id}/favorito/{restaurante_id}")
def remover_favorito(id: int, restaurante_id: int):
    if id in db_favoritos and restaurante_id in db_favoritos[id]:
        db_favoritos[id].remove(restaurante_id)
        return {"cliente_id": id, "favoritos": db_favoritos[id]}
    raise HTTPException(status_code=404, detail="Favorito não encontrado")