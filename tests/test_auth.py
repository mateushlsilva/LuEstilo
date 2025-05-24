def test_register_client(client):
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "senha": "stRongpassword1@",
        "nome": "Usuário Teste",
        "cpf": "37896412366",
        "telefone": "12982735674",
    })
    assert response.status_code == 200


def test_login_user(client):
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "senha": "stRongpassword1@"
    })
    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert "refresh_token" in json_data

    global REFRESH_TOKEN
    REFRESH_TOKEN = json_data["refresh_token"]


def test_refresh_token(client):
    response = client.post("/auth/refresh-token", json={
        "refresh_token": REFRESH_TOKEN
    })
    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"
