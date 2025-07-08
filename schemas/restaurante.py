from decimal import Decimal
from pydantic import BaseModel

class RestauranteBase(BaseModel):
    nome: str
    telefone: str
    tipo_restaurante: str
    localizacao: str
    avaliacao: float = 0.0
    saldo: Decimal = Decimal("0.00")
    disponivel: bool = False

class RestauranteCreate(RestauranteBase):
    usuario_id: int

class RestauranteRead(RestauranteBase):
    restaurante_id: int
    usuario_id: int

    class Config:
        from_attributes = True
