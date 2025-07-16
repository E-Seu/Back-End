from schemas.pedido import PedidoRead
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.entregador import Entregador
from schemas.entregador import EntregadorRead, EntregadorBase

router = APIRouter()

# Endpoints de Entregador
@router.get("/entregador/{id}", response_model=EntregadorRead)
def get_entregador(id: int, db: Session = Depends(get_db)):
    entregador = db.query(Entregador).filter(Entregador.entregador_id == id).first()
    if entregador:
        return entregador
    raise HTTPException(status_code=404, detail="Entregador não encontrado")

@router.get("/entregador/{id}/saldo")
def visualizar_saldo_entregador(id: int, db: Session = Depends(get_db)):
    entregador = db.query(Entregador).filter(Entregador.entregador_id == id).first()
    if entregador:
        return {"entregador_id": id, "saldo": float(entregador.saldo)}
    raise HTTPException(status_code=404, detail="Entregador não encontrado")

@router.put("/entregador/{id}/disponivel", response_model=EntregadorRead)
def atualizar_disponibilidade(id: int, disponivel: bool, db: Session = Depends(get_db)):
    entregador = db.query(Entregador).filter(Entregador.entregador_id == id).first()
    if not entregador:
        raise HTTPException(status_code=404, detail="Entregador não encontrado")
    entregador.disponivel = disponivel
    db.commit()
    return entregador

@router.get("/entregador/usuario/{usuario_id}", response_model=EntregadorRead)
def get_entregador_by_usuario_id(usuario_id: int, db: Session = Depends(get_db)):
    entregador = db.query(Entregador).filter(Entregador.usuario_id == usuario_id).first()
    if entregador:
        return entregador
    raise HTTPException(status_code=404, detail="Entregador não encontrado")

# Rota para visualizar pedidos entregues do entregador
@router.get("/entregador/{entregador_id}/pedidos_entregues", response_model=List[PedidoRead])
def visualizar_pedidos_entregues(entregador_id: int, db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).filter(Pedido.entregador_id == entregador_id, Pedido.status == "entregue").all()
    return pedidos

# Rota para visualizar pedido entregue pelo id e entregador
@router.get("/entregador/{entregador_id}/pedido_entregue/{pedido_id}", response_model=PedidoRead)
def visualizar_pedido_entregue(entregador_id: int, pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.pedido_id == pedido_id, Pedido.entregador_id == entregador_id, Pedido.status == "entregue").first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido entregue não encontrado para este entregador")
    return pedido

@router.put("/entregador/{id}/saldo")
def atualizar_saldo_entregador(id: int, saldo: float, db: Session = Depends(get_db)):
    entregador = db.query(Entregador).filter(Entregador.entregador_id == id).first()
    if not entregador:
        raise HTTPException(status_code=404, detail="Entregador não encontrado")
    entregador.saldo = saldo
    db.commit()
    return {"entregador_id": id, "saldo": float(entregador.saldo)}

@router.post("/entregador", response_model=EntregadorRead)
def criar_entregador(entregador: EntregadorBase, db: Session = Depends(get_db)):
    novo_entregador = Entregador(**entregador.model_dump())
    db.add(novo_entregador)
    db.commit()
    db.refresh(novo_entregador)
    return novo_entregador

# Rota para entregador aceitar pedido
@router.put("/entregador/{entregador_id}/aceitar_pedido/{pedido_id}")
def aceitar_pedido(entregador_id: int, pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.pedido_id == pedido_id).first()
    entregador = db.query(Entregador).filter(Entregador.entregador_id == entregador_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if not entregador:
        raise HTTPException(status_code=404, detail="Entregador não encontrado")
    if pedido.entregador_id is not None:
        raise HTTPException(status_code=400, detail="Pedido já foi aceito por outro entregador")
    pedido.entregador_id = entregador_id
    pedido.status = "a_caminho"
    db.commit()
    return {"pedido_id": pedido_id, "entregador_id": entregador_id, "status": pedido.status}


# Rota para entregador finalizar entrega do pedido
@router.put("/entregador/{entregador_id}/entregar_pedido/{pedido_id}")
def entregar_pedido(entregador_id: int, pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.pedido_id == pedido_id).first()
    entregador = db.query(Entregador).filter(Entregador.entregador_id == entregador_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if not entregador:
        raise HTTPException(status_code=404, detail="Entregador não encontrado")
    if pedido.entregador_id != entregador_id:
        raise HTTPException(status_code=403, detail="Este pedido não está vinculado a este entregador")
    pedido.status = "entregue"
    db.commit()
    return {"pedido_id": pedido_id, "entregador_id": entregador_id, "status": pedido.status}
from models.pedido import Pedido


# Rota para entregador rejeitar pedido (apenas para controle de tela, não altera o banco)
@router.put("/entregador/{entregador_id}/rejeitar_pedido/{pedido_id}")
def rejeitar_pedido(entregador_id: int, pedido_id: int):
    # Não altera nada no banco, apenas retorna sucesso para o frontend remover da tela
    return {"pedido_id": pedido_id, "entregador_id": entregador_id, "rejeitado": True}