from pydantic import BaseModel

class FavoritoBase(BaseModel):
    cliente_id: int
    restaurante_id: int

class FavoritoCreate(FavoritoBase):
    pass

class FavoritoRead(FavoritoBase):
    class Config:
        from_attributes = True