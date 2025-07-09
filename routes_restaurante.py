from fastapi import APIRouter, HTTPException
from schemas.restaurante import RestauranteRead
from schemas.produto import ProdutoRead, ProdutoCreate, ProdutoBase
from typing import List

router = APIRouter()

# Mock data para exemplo
db_restaurantes = [
    {
        "restaurante_id": 1,
        "usuario_id": 1,
        "nome": "Restaurante Sabor Caseiro",
        "info": "Comida caseira brasileira feita com amor",
        "local": "Rua das Flores, 123",
        "email": "saborcaseiro@email.com",
        "horario_abertura": "11:00",
        "horario_fechamento": "22:00",
        "numero_estrelas": 4.5,
        "disponivel": True,
        "telefone": "11999999999",
        "tipo_restaurante": "Brasileira",
        "saldo": "1000.00"
    },
    {
        "restaurante_id": 2,
        "usuario_id": 2,
        "nome": "Pizzaria Bella Massa",
        "info": "Pizzas tradicionais italianas",
        "local": "Av. Central, 456",
        "email": "bellamassa@email.com",
        "horario_abertura": "18:00",
        "horario_fechamento": "23:00",
        "numero_estrelas": 4.8,
        "disponivel": False,
        "telefone": "11888888888",
        "tipo_restaurante": "Italiana",
        "saldo": "500.00"
    }
]
db_produtos = [
    {
        "produto_id": 1,
        "restaurante_id": 1,
        "nome": "Feijoada",
        "descricao": "Feijoada completa com arroz, couve e farofa",
        "valor": "49.90",
        "tempo_preparo": 40,
        "disponivel": True,
        "restricoes": ["sem glúten disponível"]
    },
    {
        "produto_id": 2,
        "restaurante_id": 2,
        "nome": "Pizza Margherita",
        "descricao": "Pizza tradicional italiana com molho de tomate, mussarela e manjericão",
        "valor": "39.90",
        "tempo_preparo": 25,
        "disponivel": True,
        "restricoes": ["vegetariano"]
    }
]

# Endpoints de Restaurante
@router.get("/restaurantes/{id}", response_model=RestauranteRead)
def get_restaurante(id: int):
    for r in db_restaurantes:
        if r["restaurante_id"] == id:
            return r
    raise HTTPException(status_code=404, detail="Restaurante não encontrado")

@router.get("/restaurantes", response_model=List[RestauranteRead])
def listar_restaurantes():
    return db_restaurantes

@router.get("/restaurantes/{id}/saldo")
def visualizar_saldo_restaurante(id: int):
    for r in db_restaurantes:
        if r["restaurante_id"] == id:
            return {"restaurante_id": id, "saldo": r["saldo"]}
    raise HTTPException(status_code=404, detail="Restaurante não encontrado")

@router.get("/restaurantes/{id}/produtos", response_model=List[ProdutoRead])
def listar_produtos(id: int):
    produtos = [p for p in db_produtos if p["restaurante_id"] == id]
    return produtos

@router.post("/restaurantes/{id}/produto", response_model=ProdutoRead)
def adicionar_produto(id: int, produto: ProdutoCreate):
    novo_id = len(db_produtos) + 1
    novo_produto = produto.model_dump()
    novo_produto.update({"produto_id": novo_id, "restaurante_id": id})
    db_produtos.append(novo_produto)
    return novo_produto

@router.put("/restaurantes/{id}/disponivel", response_model=RestauranteRead)
def atualizar_disponibilidade_restaurante(id: int, disponivel: bool):
    for r in db_restaurantes:
        if r["restaurante_id"] == id:
            r["disponivel"] = disponivel
            return r
    raise HTTPException(status_code=404, detail="Restaurante não encontrado")

@router.put("/restaurantes/{id}/produto/{produto_id}", response_model=ProdutoRead)
def editar_produto(id: int, produto_id: int, produto: ProdutoBase):
    for p in db_produtos:
        if p["produto_id"] == produto_id and p["restaurante_id"] == id:
            p.update(produto.model_dump())
            return p
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@router.put("/restaurantes/{id}/produto/{produto_id}/disponivel", response_model=ProdutoRead)
def atualizar_disponibilidade_produto(id: int, produto_id: int, disponivel: bool):
    for p in db_produtos:
        if p["produto_id"] == produto_id and p["restaurante_id"] == id:
            p["disponivel"] = disponivel
            return p
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@router.put("/restaurante/{id}/saldo")
def atualizar_saldo_restaurante(id: int, saldo: float):
    for r in db_restaurantes:
        if r["restaurante_id"] == id:
            r["saldo"] = saldo
            return {"restaurante_id": id, "saldo": saldo}
    raise HTTPException(status_code=404, detail="Restaurante não encontrado")

@router.delete("/restaurante/{id}/produto/{produto_id}")
def deletar_produto(id: int, produto_id: int):
    for p in db_produtos:
        if p["produto_id"] == produto_id and p["restaurante_id"] == id:
            db_produtos.remove(p)
            return {"detail": "Produto removido com sucesso"}