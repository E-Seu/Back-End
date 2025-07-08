from pydantic import BaseModel

class RestauranteAlunoBase(BaseModel):
    matricula: str

class RestauranteAlunoCreate(RestauranteAlunoBase):
    restaurante_id: int

class RestauranteAlunoRead(RestauranteAlunoBase):
    restaurante_id: int

    class Config:
        from_attributes = True