from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.whatsappSchema import WhatsappBase
from app.utils.validated import Validadores
from app.middleware.Authorization import Authorization
from app.services.whatsappService import WhatsappService

router = APIRouter(prefix="/whatsapp", tags=["WhatsApp"], dependencies=[Depends(Authorization(["comum", 'adm']))])
service = WhatsappService()

@router.post("/", response_model=WhatsappBase, dependencies=[Depends(Authorization(["comum",'adm']))], summary="Manda Mensagem",
description="Manda mensagem.",
responses={
    200: {"description": "Cliente criado com sucesso"},
    400: {"description": "Erro de validação ou cliente já existente"},
    403: {"description": "Acesso negado"},
})
def mandar_mensagem(mensagem: WhatsappBase):
    resultado = service.enviar_template(mensagem)

    if "error" in resultado:
        raise HTTPException(status_code=400, detail="Erro ao enviar")

    return resultado

