from flask import Flask, request, jsonify, render_template
from src.config import VERIFY_TOKEN
from src.services.whatsapp import send_message
from src.services.ai import get_smart_response

app = Flask(__name__, template_folder='templates')

# Variável simples para guardar memória no WhatsApp (Para testes rápidos)
whatsapp_memory = {}

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# --- ROTA DO SIMULADOR WEB (COM MEMÓRIA) ---
@app.route("/api/test-chat", methods=["POST"])
def test_chat():
    data = request.get_json()
    user_msg = data.get("message")
    history = data.get("history", []) # Recebe o histórico do navegador
    
    ai_response = get_smart_response(user_msg, chat_history=history)
    
    return jsonify({"response": ai_response})

# --- ROTA DO WHATSAPP (COM MEMÓRIA SIMPLES) ---
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        if data.get("object") == "whatsapp_business_account":
            entry = data["entry"][0]
            changes = entry["changes"][0]
            value = changes["value"]

            if "messages" in value:
                msg_data = value["messages"][0]
                if msg_data["type"] == "text":
                    phone = msg_data["from"]
                    body = msg_data["text"]["body"]

                    # Recupera o histórico desse número (ou cria lista vazia)
                    user_history = whatsapp_memory.get(phone, [])

                    # Chama a IA com o histórico
                    response_text = get_smart_response(body, chat_history=user_history)

                    # Salva a nova troca de mensagens na memória
                    user_history.append({"role": "USER", "message": body})
                    user_history.append({"role": "CHATBOT", "message": response_text})
                    whatsapp_memory[phone] = user_history

                    send_message(phone, response_text)

    except Exception as e:
        print(f"Erro: {e}")

    return jsonify({"status": "success"}), 200

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Erro", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)