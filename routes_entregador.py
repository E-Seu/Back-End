from fastapi import APIRouter, HTTPException
from schemas.entregador import EntregadorRead, EntregadorBase

router = APIRouter()

# Mock data para exemplo
db_entregadores = [
    {"entregador_id": 1, "usuario_id": 2, "veiculo": "moto", "avaliacao": 4.7, "saldo": "300.00", "disponivel": True}
]

# Endpoints de Entregador
@router.get("/entregador/{id}", response_model=EntregadorRead)
def get_entregador(id: int):
    for e in db_entregadores:
        if e["entregador_id"] == id:
            return e
    raise HTTPException(status_code=404, detail="Entregador não encontrado")

@router.get("/entregador/{id}/saldo")
def visualizar_saldo_entregador(id: int):
    for e in db_entregadores:
        if e["entregador_id"] == id:
            return {"entregador_id": id, "saldo": e["saldo"]}
    raise HTTPException(status_code=404, detail="Entregador não encontrado")

@router.put("/entregador/{id}/disponivel", response_model=EntregadorRead)
def atualizar_disponibilidade(id: int, disponivel: bool):
    for e in db_entregadores:
        if e["entregador_id"] == id:
            e["disponivel"] = disponivel
            return e
    raise HTTPException(status_code=404, detail="Entregador não encontrado")

@router.put("/entregador/{id}/saldo")
def atualizar_saldo_entregador(id: int, saldo: float):
    for e in db_entregadores:
        if e["entregador_id"] == id:
            e["saldo"] = str(saldo)
            return {"entregador_id": id, "saldo": str(saldo)}
    raise HTTPException(status_code=404, detail="Entregador não encontrado")

@router.post("/entregador", response_model=EntregadorRead)
def criar_entregador(entregador: EntregadorBase):
    novo_id = len(db_entregadores) + 1
    novo_entregador = entregador.model_dump()
    novo_entregador["entregador_id"] = novo_id
    novo_entregador["usuario_id"] = novo_id  # Simulação
    db_entregadores.append(novo_entregador)
    return novo_entregador
