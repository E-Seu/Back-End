from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

from typing import List
from schemas.pedido_produto import PedidoProdutoCreate, PedidoProdutoRead

class PedidoBase(BaseModel):
    cliente_id: int
    restaurante_id: int
    entregador_id: Optional[int] = None
    status: str
    preco_total: Decimal = Decimal("0.00")
    localizacao: str
    data_hora: datetime
    observacao: Optional[str] = None

class PedidoCreate(PedidoBase):
    produtos: List[PedidoProdutoCreate]

class PedidoRead(PedidoBase):
    pedido_id: int
    pedido_produtos: List[PedidoProdutoRead]

    class Config:
        from_attributes = True