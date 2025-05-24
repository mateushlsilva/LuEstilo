from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.whatsappSchema import WhatsappBase
from app.utils.validated import Validadores
from app.middleware.Authorization import Authorization
from app.services.whatsappService import WhatsappService

router = APIRouter(prefix="/whatsapp", tags=["WhatsApp"], dependencies=[Depends(Authorization(["comum", 'adm']))])
service = WhatsappService()

@router.post("/", response_model=WhatsappBase, dependencies=[Depends(Authorization(["comum",'adm']))], summary="Envio de mensagem via WhatsApp",
description="""
Envia uma mensagem utilizando via WhatsApp.
A requisição deve conter as informações necessárias para o envio,
como o número do cliente e a mensagem.
""",
responses={
    200: {"description": "Mensagem enviada com sucesso."},
    400: {"description": "Erro de validação dos dados ou falha no envio da mensagem."},
    403: {"description": "Acesso negado. O usuário não tem permissão."},
})
def mandar_mensagem(mensagem: WhatsappBase):
    resultado = service.enviar_template(mensagem)

    if "error" in resultado:
        raise HTTPException(status_code=400, detail="Erro ao enviar")

    return resultado

