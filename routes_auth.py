from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from models.usuario import Usuario
from schemas.usuario import UsuarioCreate, UsuarioRead
from pydantic import BaseModel, EmailStr
from decimal import Decimal
from typing import Optional

router = APIRouter()

class AuthRequest(BaseModel):
    email: EmailStr
    senha: str

# Schema específico para registro de restaurante
class RestauranteRegister(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    info: str
    local: str
    horario_abertura: str
    horario_fechamento: str
    telefone: Optional[str] = None
    tipo_restaurante: Optional[str] = None
    numero_estrelas: float = 0.0
    disponivel: bool = True
    saldo: float = 0.0

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
    novo_cliente = Cliente(
        usuario_id=novo_usuario.usuario_id,
        nome=usuario.nome,
        email=usuario.email,
        saldo=Decimal("0.0")
    )
    db.add(novo_cliente)
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
    novo_entregador = Entregador(
        usuario_id=novo_usuario.usuario_id,
        nome=usuario.nome,
        email=usuario.email,
        veiculo="Bicicleta",
        avaliacao=0.0,
        saldo=Decimal("0.0"),
        disponivel=True
    )
    db.add(novo_entregador)
    db.commit()
    return novo_usuario

@router.post("/auth/registrar/restaurante", response_model=UsuarioRead)
def registrar_restaurante(usuario: RestauranteRegister, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    # Criar usuário
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha,
        papel="restaurante"
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    # Criar restaurante com todos os campos
    from models.restaurante import Restaurante
    novo_restaurante = Restaurante(
        usuario_id=novo_usuario.usuario_id,
        nome=usuario.nome,
        info=usuario.info,
        local=usuario.local,
        email=usuario.email,
        horario_abertura=usuario.horario_abertura,
        horario_fechamento=usuario.horario_fechamento,
        telefone=usuario.telefone,
        tipo_restaurante=usuario.tipo_restaurante,
        numero_estrelas=usuario.numero_estrelas,
        disponivel=usuario.disponivel,
        saldo=Decimal(str(usuario.saldo))
    )
    db.add(novo_restaurante)
    db.commit()
    db.refresh(novo_restaurante)
    
    return novo_usuario