from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Favorito(Base):
    __tablename__ = 'favoritos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.cliente_id'))
    restaurante_id = Column(Integer, ForeignKey('restaurantes.restaurante_id'))
    cliente = relationship('Cliente', back_populates='favoritos')
    restaurante = relationship('Restaurante', back_populates='favoritos')