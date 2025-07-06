from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Entregador(Base):
    __tablename__ = 'entregadores'
    entregador_id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'))
    veiculo = Column(String(50))
    avaliacao = Column(Float, default=0.0)
    saldo = Column(Float, default=0.0)
    disponivel = Column(Boolean, default=True)
    usuario = relationship('Usuario', back_populates='entregador')
    pedidos = relationship('Pedido', back_populates='entregador')
