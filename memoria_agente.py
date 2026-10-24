"""
    Testando chamar modelo com opção de guardar contexto/memória pela primeira vez
    Tipo: experiment
"""

from dotenv import load_dotenv
from together import Together
from together.types.chat import ChatCompletion

load_dotenv()
client = Together() # Se a variável com chave API não existir, cliente falha na criação

NUM_RODADAS = 3
DEFAULT_MODEL = "deepseek-ai/DeepSeek-V4.1-Flash-1017"

def conversa_chat_esquecido(prompt : str) -> str:
    
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {
                "role": "system",
                "content" :  """Você é um agente que adora saber o nome das pessoas,
                e faz seu melhor para tentar lembra-se desses nomes """
            },
            {
                "role" : "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=500,
    )
    
    return response.choices[0].message.content



def conversa_chat_alembrado(prompt : str, historico : ChatCompletion):

    msg = [
            {
                "role": "system",
                "content" :  """Você é um agente que adora saber o nome das pessoas,
                e faz seu melhor para tentar lembra-se desses nomes """
            }
        ]
    msg.extend(historico)
    msg.append(
        {
            "role" : "user",
            "content" : prompt
        }
    )

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=msg,
        temperature=0.3,
        max_tokens=3000,
        reasoning_effort="low"
    )

    return response.choices[0].message.content



def main():
    memo = input("Você quer conversar com um modelos que possua memória? [S/N] ").strip().upper()
    if memo == "N":
        print("Enviando pergunta ao modelo SEM memória ...")
        for _ in range(NUM_RODADAS):
            prompt = input("Seu prompt:")
            print()
            resposta = conversa_chat_esquecido(prompt)
            print("Resposta do modelo:\n", resposta)  
            print("#==========================================================#\n")          
    elif memo == "S".strip().upper():
        print("Enviando pergunta ao modelo COM memória ...")
        # Lista de dicts para registrar respostas anteriores
        hist = []
        for _ in range(NUM_RODADAS):
            prompt = input("Seu prompt: ")
            print()
            resposta = conversa_chat_alembrado(prompt, hist)
            hist.extend(
                    [
                        { "role" : "user",      "content" : prompt},
                        { "role" : "assistant", "content" : resposta}
                    ]
                )
            print("Resposta do modelo:\n", resposta)  
            print("#==========================================================#\n\n")    


if __name__ == "__main__":
    main()