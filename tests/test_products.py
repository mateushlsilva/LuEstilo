import pytest

@pytest.fixture
def auth_header(client):
    login_response = client.post("/auth/login", json={
        "email": "mateushls01@gmail.com",
        "senha": "mariojev"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_criar_produto(client, auth_header):
    response = client.post("/products/", headers=auth_header, json={
        "nome": "Produto Teste",
        "categoria": "Categoria Teste",
        "codigo_barras": "896541236",
        "data_validade": None,
        "descricao": None,
        "disponibilidade": False,
        "estoque_inicial": 1,
        "imagens": ["https://imagen.png"],
        "preco": 10.0,
        "secao": "Teste",
        "valor_venda": 10.0,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Produto Teste"
    assert "id" in data
    global produto_id
    produto_id = data["id"]


def test_get_by_id(client, auth_header):
    response = client.get(f"/products/{produto_id}", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == produto_id


def test_get_all_produtos(client, auth_header):
    response = client.get("/products", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_atualizar_produtos(client, auth_header):
    response = client.put(f"/products/{produto_id}", headers=auth_header, json={
        "nome": "Produto Atualizado",
        "categoria": "Categoria Teste",
        "codigo_barras": "896541236",
        "data_validade": None,
        "descricao": None,
        "disponibilidade": False,
        "estoque_inicial": 1,
        "imagens": ["https://imagen.png"],
        "preco": 10.0,
        "secao": "Teste",
        "valor_venda": 10.0,
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Produto Atualizado"


def test_delete_produto(client, auth_header):
    response = client.delete(f"/products/{produto_id}", headers=auth_header)
    assert response.status_code == 200
