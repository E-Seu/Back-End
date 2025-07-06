from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Cliente(Base):
    __tablename__ = 'clientes'
    cliente_id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'))
    saldo = Column(Numeric(10, 2), default=0.0)
    usuario = relationship('Usuario', back_populates='cliente')
    selos = relationship('SelosCliente', back_populates='cliente', uselist=False)
    favoritos = relationship('Favorito', back_populates='cliente')
    pedidos = relationship('Pedido', back_populates='cliente')
