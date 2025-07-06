from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    usuario_id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(20), nullable=False)
    cliente = relationship('Cliente', back_populates='usuario', uselist=False)
    entregador = relationship('Entregador', back_populates='usuario', uselist=False)
    restaurante = relationship('Restaurante', back_populates='usuario', uselist=False)
