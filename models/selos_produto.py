from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class SelosProduto(Base):
    __tablename__ = 'selos_produtos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey('produtos.produto_id'))
    sem_lactose = Column(Boolean, default=False)
    sem_gluten = Column(Boolean, default=False)
    sem_amendoim = Column(Boolean, default=False)
    vegano = Column(Boolean, default=False)
    produto = relationship('Produto', back_populates='selos')