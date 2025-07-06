from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class PedidoProduto(Base):
    __tablename__ = 'pedido_produtos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.pedido_id'))
    produto_id = Column(Integer, ForeignKey('produtos.produto_id'))
    quantidade = Column(Integer, nullable=False)
    preco_item= Column(Numeric(10, 2), nullable=False)
    pedido = relationship('Pedido', back_populates='pedido_produtos')
    produto = relationship('Produto', back_populates='pedido_produtos')