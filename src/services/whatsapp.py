import requests
from src.config import WHATSAPP_TOKEN, WHATSAPP_API_URL

def sanitize_number(number):
    """
    Garante que números do Brasil tenham o 9º dígito.
    Transforma 55718... em 557198...
    """
    if number.startswith("55") and len(number) == 12:
        return number[:4] + "9" + number[4:]
    return number

def send_message(to_number, text_body):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    # 1. Corrige o número (adiciona o 9 se faltar)
    final_number = sanitize_number(to_number)
    
    # 2. Monta a mensagem de TEXTO normal
    payload = {
        "messaging_product": "whatsapp",
        "to": final_number,
        "type": "text",
        "text": {"body": text_body}
    }

    try:
        # 3. Envia
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        
        # Logs para a gente acompanhar na Vercel
        if response.status_code in [200, 201]:
            print(f"✅ Mensagem enviada para {final_number}")
        else:
            print(f"⚠️ Erro Facebook: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")