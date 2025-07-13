from database import SessionLocal
from models.usuario import Usuario
from models.cliente import Cliente
from models.entregador import Entregador
from models.restaurante import Restaurante
from models.pedido import Pedido

# USUÁRIOS
def seed_usuarios():
    session = SessionLocal()
    if session.query(Usuario).count() == 0:
        mock_usuarios = [
            {"usuario_id": 1, "nome": "Cliente Teste", "email": "cliente@email.com", "senha": "123", "papel": "cliente"},
            {"usuario_id": 2, "nome": "Entregador Teste", "email": "entregador@email.com", "senha": "123", "papel": "entregador"},
            {"usuario_id": 3, "nome": "Restaurante Sabor Caseiro", "email": "saborcaseiro@email.com", "senha": "123", "papel": "restaurante"},
            {"usuario_id": 4, "nome": "Pizzaria Bella Massa", "email": "bellamassa@email.com", "senha": "123", "papel": "restaurante"}
        ]
        for u in mock_usuarios:
            session.add(Usuario(**u))
        session.commit()
    session.close()

# CLIENTES
def seed_clientes():
    session = SessionLocal()
    if session.query(Cliente).count() == 0:
        mock_clientes = [
            {"cliente_id": 1, "usuario_id": 1, "saldo": 200.00}
        ]
        for c in mock_clientes:
            session.add(Cliente(**c))
        session.commit()
    session.close()

# ENTREGADORES
def seed_entregadores():
    session = SessionLocal()
    if session.query(Entregador).count() == 0:
        mock_entregadores = [
            {"entregador_id": 1, "usuario_id": 2, "veiculo": "moto", "avaliacao": 4.7, "saldo": 300.00, "disponivel": True}
        ]
        for e in mock_entregadores:
            session.add(Entregador(**e))
        session.commit()
    session.close()

# RESTAURANTES
def seed_restaurantes():
    session = SessionLocal()
    if session.query(Restaurante).count() == 0:
        mock_restaurantes = [
            {
                "restaurante_id": 1,
                "usuario_id": 3,
                "nome": "Restaurante Sabor Caseiro",
                "info": "Comida caseira brasileira feita com amor",
                "local": "Rua das Flores, 123",
                "email": "saborcaseiro@email.com",
                "horario_abertura": "11:00",
                "horario_fechamento": "22:00",
                "numero_estrelas": 4.5,
                "disponivel": True,
                "telefone": "11999999999",
                "tipo_restaurante": "Brasileira",
                "saldo": 1000.00
            },
            {
                "restaurante_id": 2,
                "usuario_id": 4,
                "nome": "Pizzaria Bella Massa",
                "info": "Pizzas tradicionais italianas",
                "local": "Av. Central, 456",
                "email": "bellamassa@email.com",
                "horario_abertura": "18:00",
                "horario_fechamento": "23:00",
                "numero_estrelas": 4.8,
                "disponivel": False,
                "telefone": "11888888888",
                "tipo_restaurante": "Italiana",
                "saldo": 500.00
            }
        ]
        for r in mock_restaurantes:
            session.add(Restaurante(**r))
        session.commit()
    session.close()

# PEDIDOS
def seed_pedidos():
    session = SessionLocal()
    if session.query(Pedido).count() == 0:
        from datetime import datetime
        mock_pedidos = [
            {
                "pedido_id": 1,
                "cliente_id": 1,
                "restaurante_id": 1,
                "entregador_id": 1,
                "status": "em preparo",
                "preco_total": 80.00,
                "localizacao": "Rua das Flores, 123",
                "data_hora": datetime.now(),
                "observacao": "Sem cebola"
            },
            {
                "pedido_id": 2,
                "cliente_id": 1,
                "restaurante_id": 2,
                "entregador_id": None,
                "status": "aguardando",
                "preco_total": 45.00,
                "localizacao": "Av. Central, 456",
                "data_hora": datetime.now(),
                "observacao": None
            }
        ]
        for p in mock_pedidos:
            session.add(Pedido(**p))
        session.commit()
    session.close()

