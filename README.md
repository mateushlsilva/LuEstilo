# 🛒 Sistema de Gerenciamento de Pedidos e Produtos

API RESTful desenvolvida com **FastAPI** para controle de produtos, pedidos e usuários (clientes e administradores).

---

## 🚀 Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/mateushlsilva/LuEstilo.git
cd LuEstilo
```
### 2. Variáveis de ambiente
| Variável                      | Descrição                                                       | Exemplo                                              |
| ----------------------------- | --------------------------------------------------------------- | ---------------------------------------------------- |
| `SENTRY_DSN`                  | DSN do Sentry para rastreamento de erros                        | `https://<chave>@<host>.sentry.io/<projeto>`         |
| `SQLALCHEMY_DATABASE_URL`     | URL de conexão com o banco de dados PostgreSQL                  | `postgresql://postgres:senha@postgres:5432/postgres` |
| `JWT_SECRET_KEY`              | Chave secreta para gerar tokens JWT                             | `sua_chave_ultrasecreta`                             |
| `ALGORITHM`                   | Algoritmo de criptografia do JWT                                | `HS256`                                              |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo de expiração do token de acesso (em minutos)              | `60`                                                 |
| `REFRESH_TOKEN_EXPIRE_DAYS`   | Tempo de expiração do token de refresh (em dias)                | `7`                                                  |
| `TEST_EMAIL`                  | E-mail do usuário administrador padrão (criado automaticamente) | `admin@admin.com`                                    |
| `TEST_SENHA`                  | Senha do usuário administrador padrão                           | `admin123`                                           |


### 3. Suba os containers
```bash
docker compose up -d
```

### Tipos de Usuários
#### 🛠️ Administrador (adm)
* Gerencia Usuários (CRUD completo)
* Gerencia produtos (CRUD completo)
* Acompanha e atualiza pedidos

#### 👤 Cliente (comum)
* Consulta produtos disponíveis
* Realiza pedidos e consulta seus pedidos

### 👤 Usuário Administrador padrão

```json
{
  "email": "admin@admin.com",
  "senha": "admin"
}
```
Use esse login para acessar rotas restritas a administradores.

#### 📌 Endpoints principais
* Documentação Swagger: http://localhost:8000/docs

* Redoc: http://localhost:8000/redoc


### ✅ Pré-requisitos
* Docker
* Docker Compose


