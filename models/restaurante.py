from sqlalchemy import Column, Integer, String, ForeignKey, Float, Numeric, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Restaurante(Base):
    __tablename__ = 'restaurantes'
    restaurante_id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'))
    nome = Column(String(100), nullable=False)
    info = Column(String(255), nullable=False)  # Descrição/informações do restaurante
    local = Column(String(255), nullable=False)  # Localização
    email = Column(String(100), nullable=False)  # Email do usuário cadastrado
    horario_abertura = Column(String(5), nullable=False)  # Ex: "07:00"
    horario_fechamento = Column(String(5), nullable=False)  # Ex: "18:00"
    numero_estrelas = Column(Float, default=0.0)
    disponivel = Column(Boolean, default=True)
    telefone = Column(String(20), nullable=True)
    tipo_restaurante = Column(String(50), nullable=True)
    saldo = Column(Numeric(10, 2), default=0.0)
    usuario = relationship('Usuario', back_populates='restaurante')
    produtos = relationship('Produto', back_populates='restaurante')
    pedidos = relationship('Pedido', back_populates='restaurante')
    restaurante_alunos = relationship('RestauranteAluno', back_populates='restaurante')
    favoritos = relationship('Favorito', back_populates='restaurante')