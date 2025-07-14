from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.pedido import Pedido
from schemas.pedido import PedidoRead, PedidoCreate, PedidoBase
from typing import List
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

# Schema para atualizar status
class StatusRequest(BaseModel):
    status: str

# Endpoints de Pedido
@router.get("/pedidos/{id}", response_model=PedidoRead)
def acompanhar_pedido(id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.pedido_id == id).first()
    if pedido:
        return pedido
    raise HTTPException(status_code=404, detail="Pedido não encontrado")

@router.get("/pedidos/historico/{usuario_id}", response_model=List[PedidoRead])
def historico_pedidos(usuario_id: int, db: Session = Depends(get_db)):
    historico = db.query(Pedido).filter(Pedido.cliente_id == usuario_id).all()
    return historico

@router.post("/pedidos", response_model=PedidoRead)
def criar_pedido(pedido: PedidoBase, db: Session = Depends(get_db)):
    novo_pedido = Pedido(**pedido.model_dump())
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido

@router.put("/pedidos/{id}/status")
def atualizar_status_pedido(id: int, dados: StatusRequest, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.pedido_id == id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    pedido.status = dados.status
    db.commit()
    return {"pedido_id": id, "novo_status": dados.status}

@router.put("/pedidos/{id}/cancelar")
def cancelar_pedido(id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.pedido_id == id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    pedido.status = "cancelado"
    db.commit()
    return {"pedido_id": id, "novo_status": "cancelado"}