from pydantic import BaseModel

class PedidoProdutoBase(BaseModel):
    quantidade: int
    preco_item: Decimal = Decimal("0.00")

class PedidoProdutoCreate(PedidoProdutoBase):
    pedido_id: int
    produto_id: int

class PedidoProdutoRead(PedidoProdutoBase):
    pedido_id: int
    produto_id: int

    class Config:
        orm_mode = True