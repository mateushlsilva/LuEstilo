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


def test_create_cliente(client, auth_header):
    response = client.post("/clients/", headers=auth_header, json={
        "nome": "Cliente Teste",
        "email": "cliente@example.com",
        "cpf": "12345678901",
        "telefone": "12999999999",
        "senha": "stRongpassword1@",
        "nivel": 'comum'
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Cliente Teste"
    assert "id" in data
    global created_cliente_id
    created_cliente_id = data["id"]


def test_get_cliente_by_id(client, auth_header):
    response = client.get(f"/clients/{created_cliente_id}", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_cliente_id


def test_get_all_clientes(client, auth_header):
    response = client.get("/clients", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_cliente(client, auth_header):
    response = client.put(f"/clients/{created_cliente_id}", headers=auth_header, json={
        "nome": "Cliente Atualizado",
        "email": "cliente@example.com",
        "cpf": "12345678901",
        "telefone": "12999999999",
        "senha": "stRongpassword1@",
        "nivel": 'comum'
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Cliente Atualizado"


def test_delete_cliente(client, auth_header):
    response = client.delete(f"/clients/{created_cliente_id}", headers=auth_header)
    assert response.status_code == 200
