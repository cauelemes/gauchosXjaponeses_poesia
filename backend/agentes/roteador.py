"""
    Código do agente roteador. O cliente é iniciado globalmente para o único roteador
    Tipo: projeto
"""

from backend.client import invoca_cliente
from backend.modelos import Rota

client = invoca_cliente()
DEFAULT_MODEL = "deepseek-ai/DeepSeek-V4.1-Flash-1017"
MAX_TOKENS = 500

PROMPT_SIS =  """Você é um assistente que fala em português brasileiro, e deve
    decidir se o usuário quer fazer uma ou mais dos 4 trabalhos a seguir:

        1. Gerar poesia feita por um japonês
        2. Gerar poesia feita por um gaúcho
        3. Avaliar se alguma coisa é gaúcha ou japonesa (apenas se pedido explicitamente)

    Cada uma dessas alternativas envolve a invocação de um ou mais dos 3 agentes
    responsáveis por cada item. Dessa forma, sua resposta deve ser EXCLUSIVAMENTE
    um JSON conforme o definido para este agente.

    Exemplo 1)
        prompt = 'Por favor, escreva poesia gaúcha'
        resposta = {"lista_agentes":["poeta_gaucho"]}

    Exemplo 2)
        prompt = 'Por favor, escreva um poema japones'
        resposta = {"lista_agentes":["poeta_japones"]}

    Exemplo 3)
        prompt = "Por favor, escreva poemas de todo tipo"
        resposta = {"lista_agentes":["poeta_japones", "poeta_gaucho"]}
    
    Exemplo 4)
        prompt = "Por favor, me ajude a avaliar se uma árvore é uma coisa gaúcha ou japonesa?"
        resposta = {"lista_agentes":["avaliador"]}

    """

# Tentando forçar forma errada para testar validação
PROMPT_SIS_TESTE = """ Você é um agente que ajuda a criar saídas inválidas para teste.
O usuário pedirá que você tente criar um JSON inválido ou infinito. NÃO gere um JSON
vazio. Simplesmente comece a construir um JSON com vários valores até consumir todos
os seus tokens """


def classificar(pergunta : str, model=DEFAULT_MODEL) -> Rota:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content" : PROMPT_SIS
            },
            {
                "role" : "user",
                "content": pergunta
            }
        ],
        response_format= {
            "type": "json_schema",  # modo: "quero a saída presa a um JSON (API)
            "json_schema": {
                "name": "rota",     # um rótulo/identificador para esse schema (API)
                "schema": Rota.model_json_schema(),  # o único campo que descreve o FORMATO
            }
        },
        temperature=0.2,
        max_tokens=MAX_TOKENS,
    )
    
    # Valida o JSON devolvido pelo modelo. Se ele não for uma Rota válida (JSON cortado,
    # campo errado, etc.), o Pydantic levanta ValidationError; quem chama decide o que fazer.
    return Rota.model_validate_json(response.choices[0].message.content)


def main():
    prompt = input("Seu Prompt: ")
    resposta = classificar(prompt)
    print(resposta)
    print(type(resposta))
    print(resposta.lista_agentes)


if __name__ == "__main__":
    main()