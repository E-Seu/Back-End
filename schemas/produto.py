from decimal import Decimal
from pydantic import BaseModel
from typing import Optional
from .selos_produto import SelosProdutoRead

class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    valor: Decimal = Decimal("0.00")
    tempo_preparo: int
    disponivel: bool = True
    selos: Optional[SelosProdutoRead] = None

class ProdutoCreate(ProdutoBase):
    restaurante_id: int

class ProdutoRead(ProdutoBase):
    produto_id: int
    restaurante_id: int

    class Config:
        from_attributes = True