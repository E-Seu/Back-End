from pydantic import BaseModel

class SelosProdutoBase(BaseModel):
    sem_lactose: bool = False
    sem_gluten: bool = False
    sem_amendoim: bool = False
    vegano: bool = False

class SelosProdutoCreate(SelosProdutoBase):
    produto_id: int

class SelosProdutoRead(SelosProdutoBase):
    produto_id: int

    class Config:
        from_attributes = True