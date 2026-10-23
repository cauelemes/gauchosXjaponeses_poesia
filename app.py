import os
from dotenv import load_dotenv
from together import Together
from modelos import Rota

load_dotenv()
client = Together()
DEFAULT_MODEL = "deepseek-ai/DeepSeek-V4.1-Flash-1017"

def classificar(pergunta : str, model=DEFAULT_MODEL) -> Rota:
    # Primeira pergunta para modelos
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content" :  """Você é um assistente que fala em português brasileiro, e deve
                decidir se o usuário quer fazer uma ou mais dos 4 trabalhos a seguir:

                    1. Gerar poesia feita por um japonês
                    2. Gerar poesia feita por um gaúcho
                    3. Avaliar se alguma coisa é gaúcha ou japonesa (apenas se pedido explicitamente)

                Cada uma dessas alternativas envolve a invocação de um ou mais dos 3 agentes
                responsáveis por cada item. Dessa forma, sua resposta deve ser EXCLUSIVAMENTE
                um JSON conforme o definido para este agente.

                Exemplo 1)
                    prompt = 'Por favor, escreva poesia gaúcha'
                    resposta = {"agentes":["poeta_gaucho"]}

                Exemplo 2)
                    prompt = 'Por favor, escreva um poema japones'
                    resposta = {"agentes":["poeta_japones"]}

                Exemplo 3)
                    prompt = "Por favor, escreva poemas de todo tipo"
                    resposta = {"agentes":["poeta_japones", "poeta_gaucho"]}
                
                Exemplo 4)
                    prompt = "Por favor, me ajude a avaliar se uma árvore é uma coisa gaúcha ou japonesa?"
                    resposta = {"agentes":["avaliador"]}

                """
            },
            {
                "role" : "user",
                "content": pergunta
            }
        ],
        response_format= {
            "type": "json_schema",
            "json_schema": {
                "name": "rota",
                "schema": Rota.model_json_schema(),
            }
        },
        temperature=0.2,
        max_tokens=3000,
    )


    return response.choices[0].message.content


def main():
    prompt = input("Seu Prompt: ")
    print(classificar(prompt))


main()