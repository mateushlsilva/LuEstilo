import pytest
from app.config import settings

@pytest.fixture
def auth_header(client):
    login_response = client.post("/auth/login", json={
        "email": settings.TEST_EMAIL,
        "senha": settings.TEST_SENHA
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_criar_pedido(client, auth_header):
    response = client.post("/orders/", headers=auth_header, json={
        "periodo": "manhã",
        "secao_produtos": "eletrônica",
        "status": "pendente",
        "id_cliente": 3,
        "itens": [
            {
            "id_produto": 10,
            "quantidade": 1
            }
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["periodo"] == "manhã"
    global pedido_id
    pedido_id = data["id_pedido"]


def test_get_by_id(client, auth_header):
    response = client.get(f"/orders/{pedido_id}", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["id_pedido"] == pedido_id


def test_get_all_pedidos(client, auth_header):
    response = client.get("/orders", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_atualizar_pedido(client, auth_header):
    response = client.put(f"/orders/{pedido_id}", headers=auth_header, json={
        "periodo": "noite",
        "secao_produtos": "eletrônica",
        "status": "pendente",
        "id_cliente": 3,
        "itens": [
            {
            "id_produto": 10,
            "quantidade": 1
            }
        ]
    })
    assert response.status_code == 200
    assert response.json()["periodo"] == "noite"


def test_delete_pedido(client, auth_header):
    response = client.delete(f"/orders/{pedido_id}", headers=auth_header)
    assert response.status_code == 200
