from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

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
    pass

class PedidoRead(PedidoBase):
    pedido_id: int

    class Config:
        from_attributes = True