import os
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

WHATSAPP_API_URL = f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_ID}/messages"

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not all([WHATSAPP_TOKEN, WHATSAPP_PHONE_ID, VERIFY_TOKEN, COHERE_API_KEY]):
    print(" AVISO: Algumas variáveis de ambiente não foram configuradas no arquivo .env")