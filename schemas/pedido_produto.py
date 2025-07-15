from decimal import Decimal
from pydantic import BaseModel

from typing import Optional
from schemas.produto import ProdutoRead

class PedidoProdutoBase(BaseModel):
    produto_id: int
    quantidade: int
    preco_item: Decimal = Decimal("0.00")

class PedidoProdutoCreate(PedidoProdutoBase):
    pass

class PedidoProdutoRead(PedidoProdutoBase):
    id: int
    produto: Optional[ProdutoRead]

    class Config:
        from_attributes = True