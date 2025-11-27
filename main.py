from flask import Flask, request, jsonify, render_template
from src.config import VERIFY_TOKEN
from src.services.whatsapp import send_message
from src.services.ai import get_smart_response

# Precisamos dizer ao Flask onde está a pasta templates
app = Flask(__name__, template_folder='templates')

# --- ROTA PARA O SIMULADOR WEB (Visualizar no navegador) ---
@app.route("/", methods=["GET"])
def home():
    # Agora, ao entrar no site, carrega o nosso chat falso
    return render_template("index.html")

# --- ROTA API PARA O SIMULADOR (O HTML fala com essa rota) ---
@app.route("/api/test-chat", methods=["POST"])
def test_chat():
    data = request.get_json()
    user_msg = data.get("message")
    
    # Chama a mesma inteligência que o WhatsApp usaria
    ai_response = get_smart_response(user_msg)
    
    return jsonify({"response": ai_response})

# --- ROTA DE VERIFICAÇÃO (Oficial do WhatsApp) ---
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Erro de verificação", 403

# --- ROTA DE RECEBIMENTO (Oficial do WhatsApp) ---
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        if data.get("object") == "whatsapp_business_account":
            entry = data["entry"][0]
            changes = entry["changes"][0]
            value = changes["value"]

            if "messages" in value:
                message_data = value["messages"][0]
                if message_data["type"] == "text":
                    from_number = message_data["from"]
                    msg_body = message_data["text"]["body"]

                    # Usa a mesma IA do teste
                    ai_response = get_smart_response(msg_body)
                    send_message(from_number, ai_response)

    except Exception as e:
        print(f"Erro: {e}")

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)