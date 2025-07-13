from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.restaurante import Restaurante
from models.produto import Produto
from schemas.restaurante import RestauranteRead
from schemas.produto import ProdutoRead, ProdutoCreate
from typing import List

router = APIRouter()

# Endpoints de Restaurante
@router.get("/restaurantes/{id}", response_model=RestauranteRead)
def get_restaurante(id: int, db: Session = Depends(get_db)):
    restaurante = db.query(Restaurante).filter(Restaurante.restaurante_id == id).first()
    if restaurante:
        return restaurante
    raise HTTPException(status_code=404, detail="Restaurante não encontrado")

@router.get("/restaurantes", response_model=List[RestauranteRead])
def listar_restaurantes(db: Session = Depends(get_db)):
    return db.query(Restaurante).all()

@router.get("/restaurantes/{id}/saldo")
def visualizar_saldo_restaurante(id: int, db: Session = Depends(get_db)):
    restaurante = db.query(Restaurante).filter(Restaurante.restaurante_id == id).first()
    if restaurante:
        return {"restaurante_id": id, "saldo": float(restaurante.saldo)}
    raise HTTPException(status_code=404, detail="Restaurante não encontrado")

@router.get("/restaurantes/{id}/produtos", response_model=List[ProdutoRead])
def listar_produtos(id: int, db: Session = Depends(get_db)):
    produtos = db.query(Produto).filter(Produto.restaurante_id == id).all()
    return produtos

@router.post("/restaurantes/{id}/produto", response_model=ProdutoRead)
def adicionar_produto(id: int, produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = Produto(**produto.model_dump(), restaurante_id=id)
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@router.put("/restaurantes/{id}/disponivel", response_model=RestauranteRead)
def atualizar_disponibilidade_restaurante(id: int, disponivel: bool, db: Session = Depends(get_db)):
    restaurante = db.query(Restaurante).filter(Restaurante.restaurante_id == id).first()
    if not restaurante:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    restaurante.disponivel = disponivel
    db.commit()
    return restaurante

@router.put("/restaurantes/{id}/produto/{produto_id}", response_model=ProdutoRead)
def editar_produto(id: int, produto_id: int, produto: ProdutoCreate, db: Session = Depends(get_db)):
    produto_db = db.query(Produto).filter(Produto.produto_id == produto_id, Produto.restaurante_id == id).first()
    if not produto_db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    for key, value in produto.model_dump().items():
        setattr(produto_db, key, value) if value is not None else None

    db.commit()
    db.refresh(produto_db)
    return produto_db

@router.put("/restaurantes/{id}/produto/{produto_id}/disponivel", response_model=ProdutoRead)
def atualizar_disponibilidade_produto(id: int, produto_id: int, disponivel: bool, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.produto_id == produto_id, Produto.restaurante_id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    produto.disponivel = disponivel
    db.commit()
    return produto

@router.put("/restaurante/{id}/saldo")
def atualizar_saldo_restaurante(id: int, saldo: float, db: Session = Depends(get_db)):
    restaurante = db.query(Restaurante).filter(Restaurante.restaurante_id == id).first()
    if not restaurante:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    restaurante.saldo = saldo
    db.commit()
    return {"restaurante_id": id, "saldo": saldo}

@router.delete("/restaurante/{id}/produto/{produto_id}")
def deletar_produto(id: int, produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.produto_id == produto_id, Produto.restaurante_id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()
    return {"detail": "Produto removido com sucesso"}
