from decimal import Decimal
from pydantic import BaseModel
from typing import Optional
from .selos_produto import SelosProdutoRead, SelosProdutoBase

class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    preco: Decimal = Decimal("0.00")  # Mudança: valor -> preco
    tempo_preparo: int
    disponivel: bool = True
    selos: Optional[SelosProdutoBase] = None

class ProdutoCreate(ProdutoBase):
    restaurante_id: int

class ProdutoRead(ProdutoBase):
    produto_id: int
    restaurante_id: int
    selos: Optional[SelosProdutoRead] = None

    class Config:
        from_attributes = True