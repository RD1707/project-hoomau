import requests
from src.config import WHATSAPP_TOKEN, WHATSAPP_API_URL

def sanitize_number(number):
    """
    Força a adição do 9º dígito em números de celular do Brasil (DDD > 29 ou gerais).
    Transforma 557183000082 -> 5571983000082
    """
    # Se for Brasil (55) e tiver 12 dígitos (DDD + 8 números), ENFIA O 9
    if number.startswith("55") and len(number) == 12:
        return number[:4] + "9" + number[4:]
    return number

def send_message(to_number, text_body):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    # 1. Calcula a versão do número COM o 9º dígito
    corrected_number = sanitize_number(to_number)

    # 2. Se o número mudou (ou seja, precisava do 9), tenta enviar para o CORRIGIDO primeiro
    if corrected_number != to_number:
        print(f"🔄 Forçando envio para número com 9º dígito: {corrected_number}")
        if _try_send(corrected_number, text_body, headers):
            return # Se deu certo com o 9, para aqui.

    # 3. Se falhar (ou se não precisava corrigir), tenta o original
    print(f"🔄 Tentando envio para número original: {to_number}")
    _try_send(to_number, text_body, headers)

def _try_send(to_number, text_body, headers):
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": text_body}
    }

    try:
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        response_json = response.json()

        if response.status_code in [200, 201]:
            print(f"✅ SUCESSO! Facebook aceitou envio para {to_number}")
            return True
        
        print(f"⚠️ Falha ao enviar para {to_number}: {response.status_code}")
        print(f"Erro FB: {response.text}")
        return False

    except Exception as e:
        print(f"❌ Erro crítico de conexão: {e}")
        return False