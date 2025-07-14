from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.restaurante import Restaurante
from models.produto import Produto
from schemas.restaurante import RestauranteRead
from schemas.produto import ProdutoRead, ProdutoCreate, ProdutoBase
from typing import List
from decimal import Decimal
from pydantic import BaseModel

router = APIRouter()

# Schema para receber o valor de disponibilidade
class DisponibilidadeRequest(BaseModel):
    disponivel: bool

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
def adicionar_produto(id: int, produto: ProdutoBase, db: Session = Depends(get_db)):
    # Verificar se restaurante existe
    restaurante = db.query(Restaurante).filter(Restaurante.restaurante_id == id).first()
    if not restaurante:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    
    # Criar produto diretamente
    novo_produto = Produto(
        restaurante_id=id,
        nome=produto.nome,
        descricao=produto.descricao,
        preco=Decimal(str(produto.preco)),  # Agora ambos usam 'preco'
        tempo_preparo=produto.tempo_preparo,
        disponivel=produto.disponivel
    )
    
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    
    # Adicionar selos se fornecidos
    if produto.selos:
        from models.selos_produto import SelosProduto
        novo_selo = SelosProduto(
            produto_id=novo_produto.produto_id,
            sem_lactose=produto.selos.sem_lactose,
            sem_gluten=produto.selos.sem_gluten,
            sem_amendoim=produto.selos.sem_amendoim,
            vegano=produto.selos.vegano
        )
        db.add(novo_selo)
        db.commit()
        db.refresh(novo_produto)
    
    return novo_produto

@router.put("/restaurantes/{id}/disponivel", response_model=RestauranteRead)
def atualizar_disponibilidade_restaurante(id: int, dados: DisponibilidadeRequest, db: Session = Depends(get_db)):
    restaurante = db.query(Restaurante).filter(Restaurante.restaurante_id == id).first()
    if not restaurante:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    restaurante.disponivel = dados.disponivel
    db.commit()
    db.refresh(restaurante)
    return restaurante

@router.put("/restaurantes/{id}/produto/{produto_id}", response_model=ProdutoRead)
def editar_produto(id: int, produto_id: int, produto: ProdutoBase, db: Session = Depends(get_db)):
    produto_db = db.query(Produto).filter(Produto.produto_id == produto_id, Produto.restaurante_id == id).first()
    if not produto_db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Atualizar campos do produto
    produto_db.nome = produto.nome
    produto_db.descricao = produto.descricao
    produto_db.preco = Decimal(str(produto.preco))  # Agora ambos usam 'preco'
    produto_db.tempo_preparo = produto.tempo_preparo
    produto_db.disponivel = produto.disponivel

    # Atualizar selos se fornecidos
    if produto.selos:
        from models.selos_produto import SelosProduto
        selo_existente = db.query(SelosProduto).filter(SelosProduto.produto_id == produto_id).first()
        if selo_existente:
            selo_existente.sem_lactose = produto.selos.sem_lactose
            selo_existente.sem_gluten = produto.selos.sem_gluten
            selo_existente.sem_amendoim = produto.selos.sem_amendoim
            selo_existente.vegano = produto.selos.vegano
        else:
            novo_selo = SelosProduto(
                produto_id=produto_id,
                sem_lactose=produto.selos.sem_lactose,
                sem_gluten=produto.selos.sem_gluten,
                sem_amendoim=produto.selos.sem_amendoim,
                vegano=produto.selos.vegano
            )
            db.add(novo_selo)

    db.commit()
    db.refresh(produto_db)
    return produto_db

@router.put("/restaurantes/{id}/produto/{produto_id}/disponivel", response_model=ProdutoRead)
def atualizar_disponibilidade_produto(id: int, produto_id: int, dados: DisponibilidadeRequest, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.produto_id == produto_id, Produto.restaurante_id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    produto.disponivel = dados.disponivel
    db.commit()
    db.refresh(produto)
    return produto

@router.put("/restaurante/{id}/saldo")
def atualizar_saldo_restaurante(id: int, saldo: float, db: Session = Depends(get_db)):
    restaurante = db.query(Restaurante).filter(Restaurante.restaurante_id == id).first()
    if not restaurante:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")
    restaurante.saldo = Decimal(str(saldo))
    db.commit()
    db.refresh(restaurante)
    return {"restaurante_id": id, "saldo": float(restaurante.saldo)}

@router.delete("/restaurante/{id}/produto/{produto_id}")
def deletar_produto(id: int, produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.produto_id == produto_id, Produto.restaurante_id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()
    return {"detail": "Produto removido com sucesso"}