from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class RestauranteAluno(Base):
    __tablename__ = 'restaurantes_alunos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurante_id = Column(Integer, ForeignKey('restaurantes.restaurante_id'))
    matricula = Column(Integer, nullable=False)
    restaurante = relationship('Restaurante', back_populates='restaurante_alunos')
