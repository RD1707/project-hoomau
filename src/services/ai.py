import cohere
from src.config import COHERE_API_KEY
from src.utils.prompts import HOOMAU_SYSTEM_PROMPT

# Inicializa o cliente do Cohere
co = cohere.Client(COHERE_API_KEY)

def get_smart_response(user_message, chat_history=[]):
    """
    Envia a mensagem + o histórico da conversa para a IA ter contexto.
    """
    try:
        response = co.chat(
            model='command-r',
            message=user_message,
            preamble=HOOMAU_SYSTEM_PROMPT,
            temperature=2.2, # Baixa criatividade para não alucinar, mas não robótico
            chat_history=chat_history # <--- AQUI ESTÁ A MEMÓRIA
        )
        
        return response.text

    except Exception as e:
        print(f"Erro ao chamar Cohere: {e}")
        return "No momento estou com uma instabilidade técnica. Um atendente humano responderá em breve."