from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.cliente import Cliente
from schemas.cliente import ClienteRead
from typing import List
from models.favorito import Favorito
from models.selos_cliente import SelosCliente

router = APIRouter()

@router.get("/usuario/{usuario_id}/nome")
def get_nome_cliente(usuario_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.usuario_id == usuario_id).first()
    if not cliente or not hasattr(cliente, 'usuario') or not hasattr(cliente.usuario, 'nome'):
        raise HTTPException(status_code=404, detail="Cliente ou nome de usuário não encontrado")
    return {"usuario_id": usuario_id, "nome": cliente.usuario.nome}

# Endpoints de Cliente - usando usuario_id em vez de cliente_id
@router.get("/clientes/{id}", response_model=ClienteRead)
def get_cliente(id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.usuario_id == id).first()
    if cliente:
        return cliente
    raise HTTPException(status_code=404, detail="Cliente não encontrado")

@router.get("/clientes/{id}/favorito")
def listar_favoritos(id: int, db: Session = Depends(get_db)):
    # Buscar cliente pelo usuario_id primeiro
    cliente = db.query(Cliente).filter(Cliente.usuario_id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    favoritos = db.query(Favorito).filter(Favorito.cliente_id == cliente.cliente_id).all()
    return {"usuario_id": id, "favoritos": [fav.restaurante_id for fav in favoritos]}

@router.get("/clientes/{id}/saldo")
def visualizar_saldo(id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.usuario_id == id).first()
    if cliente:
        return {"usuario_id": id, "saldo": float(cliente.saldo)}
    raise HTTPException(status_code=404, detail="Cliente não encontrado")

@router.post("/clientes/{id}/favorito/{restaurante_id}")
def adicionar_favorito(id: int, restaurante_id: int, db: Session = Depends(get_db)):
    # Buscar cliente pelo usuario_id primeiro
    cliente = db.query(Cliente).filter(Cliente.usuario_id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    favorito = db.query(Favorito).filter(Favorito.cliente_id == cliente.cliente_id, Favorito.restaurante_id == restaurante_id).first()
    if favorito:
        favoritos = db.query(Favorito).filter(Favorito.cliente_id == cliente.cliente_id).all()
        return {"usuario_id": id, "favoritos": [fav.restaurante_id for fav in favoritos]}
    
    novo_favorito = Favorito(cliente_id=cliente.cliente_id, restaurante_id=restaurante_id)
    db.add(novo_favorito)
    db.commit()
    favoritos = db.query(Favorito).filter(Favorito.cliente_id == cliente.cliente_id).all()
    return {"usuario_id": id, "favoritos": [fav.restaurante_id for fav in favoritos]}

@router.put("/clientes/{id}/restricoes")
def atualizar_restricoes(id: int, restricoes: List[str], db: Session = Depends(get_db)):
    # Buscar cliente pelo usuario_id primeiro
    cliente = db.query(Cliente).filter(Cliente.usuario_id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Remove selos antigos
    db.query(SelosCliente).filter(SelosCliente.cliente_id == cliente.cliente_id).delete()
    # Adiciona novos selos
    for restricao in restricoes:
        db.add(SelosCliente(cliente_id=cliente.cliente_id, selo=restricao))
    db.commit()
    return {"usuario_id": id, "restricoes": restricoes}

@router.put("/clientes/{id}/saldo")
def atualizar_saldo(id: int, saldo: float, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.usuario_id == id).first()
    if cliente:
        cliente.saldo = saldo
        db.commit()
        return {"usuario_id": id, "saldo": float(cliente.saldo)}
    raise HTTPException(status_code=404, detail="Cliente não encontrado")

@router.delete("/clientes/{id}/favorito/{restaurante_id}")
def remover_favorito(id: int, restaurante_id: int, db: Session = Depends(get_db)):
    # Buscar cliente pelo usuario_id primeiro
    cliente = db.query(Cliente).filter(Cliente.usuario_id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    favorito = db.query(Favorito).filter(Favorito.cliente_id == cliente.cliente_id, Favorito.restaurante_id == restaurante_id).first()
    if not favorito:
        raise HTTPException(status_code=404, detail="Favorito não encontrado")
    
    db.delete(favorito)
    db.commit()
    favoritos = db.query(Favorito).filter(Favorito.cliente_id == cliente.cliente_id).all()
    return {"usuario_id": id, "favoritos": [fav.restaurante_id for fav in favoritos]}