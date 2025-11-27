import requests
from src.config import WHATSAPP_TOKEN, WHATSAPP_API_URL

def sanitize_number(number):
    """
    Corrige números do Brasil que chegam sem o 9º dígito.
    Ex: Transforma 557183000082 em 5571983000082
    """
    # Se for Brasil (55) e tiver 12 dígitos (DDD + 8 números), adiciona o 9
    if number.startswith("55") and len(number) == 12:
        return number[:4] + "9" + number[4:]
    return number

def send_message(to_number, text_body):
    """
    Envia a mensagem, tentando corrigir o número se falhar.
    """
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    # Tentativa 1: Enviar para o número EXATO que chegou (sem mexer)
    if _try_send(to_number, text_body, headers):
        return

    # Tentativa 2: Se falhar (ou se quisermos garantir), tenta com o 9
    corrected_number = sanitize_number(to_number)
    if corrected_number != to_number:
        print(f"🔄 Tentando reenviar com 9º dígito para: {corrected_number}")
        _try_send(corrected_number, text_body, headers)

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

        # Se deu certo (Status 200 ou 201)
        if response.status_code in [200, 201]:
            print(f"✅ SUCESSO! Facebook aceitou envio para {to_number}")
            print(f"Resposta FB: {response_json}")
            return True
        
        # Se deu erro
        print(f"⚠️ Falha ao enviar para {to_number}: {response.status_code}")
        print(f"Erro FB: {response.text}")
        return False

    except Exception as e:
        print(f"❌ Erro crítico de conexão: {e}")
        return False