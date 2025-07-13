from pydantic import BaseModel, EmailStr

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioRead(UsuarioBase):
    usuario_id: int
    papel: str

    class Config:
        from_attributes = True