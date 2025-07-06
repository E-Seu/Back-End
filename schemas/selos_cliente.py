from pydantic import BaseModel

class SelosClienteBase(BaseModel):
    sem_lactose: bool = False
    sem_gluten: bool = False
    sem_amendoim: bool = False
    vegano: bool = False

class SelosClienteCreate(SelosClienteBase):
    cliente_id: int

class SelosClienteRead(SelosClienteBase):
    cliente_id: int

    class Config:
        orm_mode = True