import requests
import json
from src.config import WHATSAPP_TOKEN, WHATSAPP_API_URL

def send_message(to_number, text_body):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    # FORÇAR O NÚMERO COM 9 DÍGITOS (Padrão Brasil para receber template)
    # Se chegar 55718... transforma em 557198...
    target_number = to_number
    if target_number.startswith("55") and len(target_number) == 12:
        target_number = target_number[:4] + "9" + target_number[4:]

    print(f"🚀 Tentando enviar TEMPLATE para: {target_number}")

    # Payload para enviar o Template 'hello_world'
    # Esse template é imune a bloqueios de sessão
    payload = {
        "messaging_product": "whatsapp",
        "to": target_number,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }

    try:
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            print(f"✅ TEMPLATE ENVIADO! Status: {response.status_code}")
            return True
        
        print(f"⚠️ Erro no Template: {response.status_code} - {response.text}")
        
        # Se o template falhar, tenta o método antigo de texto como fallback
        print("🔄 Tentando mensagem de texto normal...")
        payload_text = {
            "messaging_product": "whatsapp",
            "to": target_number,
            "type": "text",
            "text": {"body": text_body}
        }
        requests.post(WHATSAPP_API_URL, headers=headers, json=payload_text)

    except Exception as e:
        print(f"❌ Erro crítico: {e}")