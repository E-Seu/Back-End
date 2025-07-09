from decimal import Decimal
from pydantic import BaseModel, EmailStr
from typing import Optional

class RestauranteBase(BaseModel):
    nome: str
    info: str  # Descrição/informações do restaurante
    local: str  # Localização
    email: EmailStr  # Email do usuário cadastrado
    horario_abertura: str  # Ex: "07:00"
    horario_fechamento: str  # Ex: "18:00"
    numero_estrelas: float = 0.0
    disponivel: bool = True
    telefone: Optional[str] = None
    tipo_restaurante: Optional[str] = None
    saldo: Decimal = Decimal("0.00")

class RestauranteCreate(RestauranteBase):
    usuario_id: int

class RestauranteRead(RestauranteBase):
    restaurante_id: int
    usuario_id: int

    class Config:
        from_attributes = True
