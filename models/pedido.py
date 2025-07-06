from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from .base import Base

class Pedido(Base):
    __tablename__ = 'pedidos'
    pedido_id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.cliente_id'))
    restaurante_id = Column(Integer, ForeignKey('restaurantes.restaurante_id'))
    entregador_id = Column(Integer, ForeignKey('entregadores.entregador_id'))
    status = Column(String(20))
    preco_total = Column(Numeric(10, 2))
    localizacao = Column(Text)
    data_hora = Column(DateTime)
    observacao = Column(Text)
    cliente = relationship('Cliente', back_populates='pedidos')
    restaurante = relationship('Restaurante', back_populates='pedidos')
    entregador = relationship('Entregador', back_populates='pedidos')
    pedido_produtos = relationship('PedidoProduto', back_populates='pedido')