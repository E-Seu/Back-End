from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.cliente import Cliente
from schemas.cliente import ClienteRead
from typing import List
from models.favorito import Favorito
from models.selos_cliente import SelosCliente

router = APIRouter()

# Endpoints de Cliente
@router.get("/clientes/{id}", response_model=ClienteRead)
def get_cliente(id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.cliente_id == id).first()
    if cliente:
        return cliente
    raise HTTPException(status_code=404, detail="Cliente não encontrado")

@router.get("/clientes/{id}/favorito")
def listar_favoritos(id: int, db: Session = Depends(get_db)):
    favoritos = db.query(Favorito).filter(Favorito.cliente_id == id).all()
    return {"cliente_id": id, "favoritos": [fav.restaurante_id for fav in favoritos]}

@router.get("/clientes/{id}/saldo")
def visualizar_saldo(id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.cliente_id == id).first()
    if cliente:
        return {"cliente_id": id, "saldo": float(cliente.saldo)}
    raise HTTPException(status_code=404, detail="Cliente não encontrado")

@router.post("/clientes/{id}/favorito/{restaurante_id}")
def adicionar_favorito(id: int, restaurante_id: int, db: Session = Depends(get_db)):
    favorito = db.query(Favorito).filter(Favorito.cliente_id == id, Favorito.restaurante_id == restaurante_id).first()
    if favorito:
        return {"cliente_id": id, "favoritos": [favorito.restaurante_id]}
    novo_favorito = Favorito(cliente_id=id, restaurante_id=restaurante_id)
    db.add(novo_favorito)
    db.commit()
    favoritos = db.query(Favorito).filter(Favorito.cliente_id == id).all()
    return {"cliente_id": id, "favoritos": [fav.restaurante_id for fav in favoritos]}

@router.put("/clientes/{id}/restricoes")
def atualizar_restricoes(id: int, restricoes: List[str], db: Session = Depends(get_db)):
    # Remove selos antigos
    db.query(SelosCliente).filter(SelosCliente.cliente_id == id).delete()
    # Adiciona novos selos
    for restricao in restricoes:
        db.add(SelosCliente(cliente_id=id, selo=restricao))
    db.commit()
    return {"cliente_id": id, "restricoes": restricoes}

@router.put("/clientes/{id}/saldo")
def atualizar_saldo(id: int, saldo: float, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.cliente_id == id).first()
    if cliente:
        cliente.saldo = saldo
        db.commit()
        return {"cliente_id": id, "saldo": float(cliente.saldo)}
    raise HTTPException(status_code=404, detail="Cliente não encontrado")

@router.delete("/clientes/{id}/favorito/{restaurante_id}")
def remover_favorito(id: int, restaurante_id: int, db: Session = Depends(get_db)):
    favorito = db.query(Favorito).filter(Favorito.cliente_id == id, Favorito.restaurante_id == restaurante_id).first()
    if not favorito:
        raise HTTPException(status_code=404, detail="Favorito não encontrado")
    db.delete(favorito)
    db.commit()
    favoritos = db.query(Favorito).filter(Favorito.cliente_id == id).all()
    return {"cliente_id": id, "favoritos": [fav.restaurante_id for fav in favoritos]}
