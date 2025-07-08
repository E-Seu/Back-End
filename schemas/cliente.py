from decimal import Decimal
from pydantic import BaseModel

class ClienteBase(BaseModel):
    saldo: Decimal = Decimal("0.00")

class ClienteCreate(ClienteBase):
    usuario_id: int

class ClienteRead(ClienteBase):
    cliente_id: int
    usuario_id: int

    class Config:
        from_attributes = True