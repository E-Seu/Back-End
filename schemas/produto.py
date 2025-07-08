from decimal import Decimal
from pydantic import BaseModel

class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    preco: Decimal = Decimal("0.00")
    tempo_preparo: int
    disponivel: bool = True

class ProdutoCreate(ProdutoBase):
    restaurante_id: int

class ProdutoRead(ProdutoBase):
    produto_id: int
    restaurante_id: int

    class Config:
        from_attributes = True
