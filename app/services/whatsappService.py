import requests
from app.config import settings
from app.schemas.whatsappSchema import WhatsappBase

class WhatsappService:
    def __init__(self):
        pass

    def enviar_template(self,mensagem: WhatsappBase):
        url = f"https://graph.facebook.com/v22.0/{settings.PHONE_NUMBER_ID}/messages"
        
        headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": mensagem.numero,
            "type": "template",
            "text": {
                "preview_url": False,
                "body": mensagem.mensagem
            }
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()