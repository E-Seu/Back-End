# Rota para listar pedidos disponíveis para entrega (status 'pronto')
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.pedido import Pedido
from schemas.pedido import PedidoRead, PedidoCreate, PedidoBase
from typing import List
from datetime import datetime
from pydantic import BaseModel
from models.pedido_produto import PedidoProduto
from schemas.pedido_produto import PedidoProdutoCreate
from sqlalchemy.orm import joinedload

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

@router.get("/pedido/disponiveis", response_model=List[PedidoRead])
def listar_pedidos_disponiveis(db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).filter(Pedido.status == "pronto").all()
    return pedidos

@router.post("/pedidos", response_model=PedidoRead)
def criar_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    # Cria o pedido
    produtos_data = pedido.produtos
    pedido_data = pedido.model_dump(exclude={"produtos"})
    novo_pedido = Pedido(**pedido_data)
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    # Cria os itens do pedido
    for item in produtos_data:
        pedido_produto = PedidoProduto(
            pedido_id=novo_pedido.pedido_id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            preco_item=item.preco_item
        )
        db.add(pedido_produto)
    db.commit()

    # Retorna o pedido com os produtos
    pedido_completo = db.query(Pedido).options(joinedload(Pedido.pedido_produtos).joinedload(PedidoProduto.produto)).filter(Pedido.pedido_id == novo_pedido.pedido_id).first()
    return pedido_completo

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