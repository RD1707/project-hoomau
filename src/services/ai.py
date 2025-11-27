import cohere
from src.config import COHERE_API_KEY
from src.utils.prompts import HOOMAU_SYSTEM_PROMPT

co = cohere.Client(COHERE_API_KEY)

def get_smart_response(user_message):
    """
    Envia a mensagem do usuário para o Cohere e retorna a resposta da IA.
    """
    try:
        response = co.chat(
            model='command-a-03-2025',
            message=user_message,
            preamble=HOOMAU_SYSTEM_PROMPT, 
            temperature=0.3 
        )
        
        return response.text

    except Exception as e:
        print(f"Erro ao chamar Cohere: {e}")
        return "No momento estou com uma instabilidade técnica. Um atendente humano responderá em breve."