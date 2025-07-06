from pydantic import BaseModel

class EntregadorBase(BaseModel):
    veiculo: str
    avaliacao: float = 0.0
    saldo: Decimal = Decimal("0.00")
    disponivel: bool = False

class EntregadorCreate(EntregadorBase):
    usuario_id: int

class EntregadorRead(EntregadorBase):
    entregador_id: int
    usuario_id: int

    class Config:
        orm_mode = True