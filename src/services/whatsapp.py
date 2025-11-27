import requests
from src.config import WHATSAPP_TOKEN, WHATSAPP_API_URL

def send_message(to_number, text_body):
    """
    Envia uma mensagem de texto para o número especificado via WhatsApp Cloud API.
    """
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {
            "body": text_body
        }
    }

    try:
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar mensagem para {to_number}: {e}")
        if response is not None:
             print(f"Detalhes: {response.text}")
        return None