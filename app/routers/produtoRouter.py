from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import Database
from app.schemas.produtoSchema import ProdutoBase, ProdutoRead, ProdutoRemove
from app.services.produtoService import ProdutoService
from app.models.produtoModel import Produto
from app.utils.validated import Validadores
from app.middleware.Authorization import Authorization


router = APIRouter(prefix="/products", tags=["Produtos"], dependencies=[Depends(Authorization(["comum", 'adm']))])
service = ProdutoService()
db = Database()


@router.get("/", response_model=List[ProdutoRead], summary="Listar produtos",
description="Retorna uma lista de produtos cadastrados com filtros opcionais por categoria, preço e disponibilidade.",
responses={
    200: {"description": "Lista de produtos retornada com sucesso"},
    403: {"description": "Acesso negado"},
})
def listar_produtos(
    categoria: Optional[str] = Query(None), 
    preco: Optional[float] = Query(None) , 
    disponibilidade: Optional[bool] = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(db.get_db)
):
    return service.pegar_todos_produtos(db, categoria, preco, disponibilidade, skip, limit)

@router.get("/{id}", response_model=ProdutoRead, summary="Buscar produto por ID",
description="Busca os detalhes de um produto específico usando o ID.",
responses={
    200: {"description": "Produto encontrado"},
    403: {"description": "Acesso negado"},
    404: {"description": "Produto não encontrado"},
})
def buscar_produto(id: int, db: Session = Depends(db.get_db)):
    produto = service.pegar_produto_id(db, id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.post("/", response_model=ProdutoRead, dependencies=[Depends(Authorization(['adm']))], summary="Criar novo produto",
description="Cria um novo produto. Requer permissão de administrador.",
responses={
    201: {"description": "Produto criado com sucesso"},
    400: {"description": "Erro de validação ou produto já existente"},
    403: {"description": "Acesso negado"},
})
def criar_produto(produto: ProdutoBase, db: Session = Depends(db.get_db)):
   
    if db.query(Produto).filter_by(codigo_barras=produto.codigo_barras).first():
        raise HTTPException(status_code=400, detail="Código de barras já cadastrado!")

    novo_produto = service.criar_produto(db, produto)
    return novo_produto

@router.delete("/{id}",  response_model=ProdutoRemove, dependencies=[Depends(Authorization(['adm']))], summary="Deletar produto",
description="Remove um produto do sistema com base no ID. Requer permissão de administrador.",
responses={
    200: {"description": "Produto deletado com sucesso"},
    404: {"description": "Produto não encontrado"},
    403: {"description": "Acesso negado"},
})
def deletar_produto(id: int, db: Session = Depends(db.get_db)):
    produto = service.deletar_produto(db, id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"detail": 'Produto deletado!'}


@router.put("/{id}", response_model=ProdutoRead, dependencies=[Depends(Authorization(['adm']))], summary="Atualizar produto",
description="Atualiza as informações de um produto existente. Requer permissão de administrador.",
responses={
    200: {"description": "Produto atualizado com sucesso"},
    400: {"description": "Erro de validação"},
    404: {"description": "Produto não encontrado"},
    403: {"description": "Acesso negado"},
})
def atualizar_produto(id: int, produto: ProdutoBase, db: Session = Depends(db.get_db)):
    try:   
        produto_atualizado = service.alterar_produto(db, id, produto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not produto_atualizado:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return produto_atualizado