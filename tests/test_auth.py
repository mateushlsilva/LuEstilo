import jwt
from app.config import settings

def test_register_login_refresh_delete(client):
    email = "test@example.com"
    senha = "stRongpassword1@"

    # Criação
    response = client.post("/auth/register", json={
        "email": email,
        "senha": senha,
        "nome": "Usuário Teste",
        "cpf": "37896412366",
        "telefone": "12982735674",
    })
    assert response.status_code in [200, 400]

    # Login
    response = client.post("/auth/login", json={"email": email, "senha": senha})
    assert response.status_code == 200
    tokens = response.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    payload = jwt.decode(
        access_token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    id_cli = payload["sub"]
    auth_header = {"Authorization": f"Bearer {access_token}"}

    # Refresh
    response = client.post("/auth/refresh-token", json={"refresh_token": refresh_token})
    assert response.status_code == 200

    # Delete
    response = client.delete(f"/clients/{id_cli}", headers=auth_header)
    assert response.status_code == 200
