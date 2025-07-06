from sqlalchemy import Column, Integer, String, ForeignKey, Float, Numeric, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Restaurante(Base):
    __tablename__ = 'restaurantes'
    restaurante_id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'))
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20))
    tipo_restaurante = Column(String(20))
    localizacao = Column(String(255))
    avaliacao = Column(Float, default=0.0)
    saldo = Column(Numeric(10, 2), default=0.0)
    disponivel = Column(Boolean, default=False)
    usuario = relationship('Usuario', back_populates='restaurante')
    produtos = relationship('Produto', back_populates='restaurante')
    pedidos = relationship('Pedido', back_populates='restaurante')
    restaurante_alunos = relationship('RestauranteAluno', back_populates='restaurante')
    favoritos = relationship('Favorito', back_populates='restaurante')