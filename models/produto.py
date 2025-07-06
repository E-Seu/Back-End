from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from .base import Base

class Produto(Base):
    __tablename__ = 'produtos'
    produto_id = Column(Integer, primary_key=True, autoincrement=True)
    restaurante_id = Column(Integer, ForeignKey('restaurantes.restaurante_id'))
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    preco = Column(Float, nullable=False)
    tempo_preparo = Column(Integer)
    disponivel = Column(Boolean, default=True)
    restaurante = relationship('Restaurante', back_populates='produtos')
    selos = relationship('SelosProduto', back_populates='produto', uselist=False)
    pedido_produtos = relationship('PedidoProduto', back_populates='produto')