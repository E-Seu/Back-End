from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class SelosCliente(Base):
    __tablename__ = 'selos_clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.cliente_id'))
    sem_lactose = Column(Boolean, default=False)
    sem_gluten = Column(Boolean, default=False)
    sem_amendoim = Column(Boolean, default=False)
    vegano = Column(Boolean, default=False)
    cliente = relationship('Cliente', back_populates='selos')