from decimal import Decimal
from pydantic import BaseModel
from typing import List, Optional

class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    valor: Decimal = Decimal("0.00")  # Mudando de 'preco' para 'valor' como no exemplo
    tempo_preparo: int
    disponivel: bool = True
    restricoes: List[str] = []  # Lista de restrições (vegetariano, sem glúten, etc)

class ProdutoCreate(ProdutoBase):
    restaurante_id: int

class ProdutoRead(ProdutoBase):
    produto_id: int
    restaurante_id: int

    class Config:
        from_attributes = True
