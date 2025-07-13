from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from models.usuario import Usuario
from schemas.usuario import UsuarioCreate, UsuarioRead
from pydantic import BaseModel, EmailStr

router = APIRouter()

class AuthRequest(BaseModel):
    email: EmailStr
    senha: str

def autenticar(email: str, senha: str, papel: str, db: Session) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.email == email, Usuario.senha == senha, Usuario.papel == papel).first()
    if usuario:
        return usuario
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

# Endpoints de Autenticação

@router.post("/auth/entregador", response_model=UsuarioRead)
def autenticar_entregador(auth: AuthRequest, db: Session = Depends(get_db)):
    return autenticar(str(auth.email), auth.senha, "entregador", db)

@router.post("/auth/restaurante", response_model=UsuarioRead)
def autenticar_restaurante(auth: AuthRequest, db: Session = Depends(get_db)):
    return autenticar(str(auth.email), auth.senha, "restaurante", db)

@router.post("/auth/cliente", response_model=UsuarioRead)
def autenticar_cliente(auth: AuthRequest, db: Session = Depends(get_db)):
    return autenticar(str(auth.email), auth.senha, "cliente", db)

@router.post("/auth/login", response_model=UsuarioRead)
def login(auth: AuthRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == str(auth.email), Usuario.senha == auth.senha).first()
    if usuario:
        return usuario
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

@router.post("/auth/registrar/cliente", response_model=UsuarioRead)
def registrar_cliente(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha,
        papel="cliente"
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    from models.cliente import Cliente
    db.add(Cliente(usuario_id=novo_usuario.usuario_id, saldo=0.0))
    db.commit()
    return novo_usuario

@router.post("/auth/registrar/entregador", response_model=UsuarioRead)
def registrar_entregador(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha,
        papel="entregador"
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    from models.entregador import Entregador
    db.add(Entregador(usuario_id=novo_usuario.usuario_id, veiculo="", avaliacao=0.0, saldo=0.0, disponivel=False))
    db.commit()
    return novo_usuario

@router.post("/auth/registrar/restaurante", response_model=UsuarioRead)
def registrar_restaurante(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha,
        papel="restaurante"
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    from models.restaurante import Restaurante
    db.add(Restaurante(
        usuario_id=novo_usuario.usuario_id,
        nome=novo_usuario.nome,
        info="",
        local="",
        email=novo_usuario.email,
        horario_abertura="",
        horario_fechamento="",
        numero_estrelas=0.0,
        disponivel=False,
        telefone=None,
        tipo_restaurante=None,
        saldo=0.0
    ))
    db.commit()
    return novo_usuario
