"""
    Módulo para invocar agentes criadores: "poeta_gaucho", "poeta_japones", "avaliador"
"""

from backend.client import client

DEFAULT_MODEL = "deepseek-ai/DeepSeek-V4.1-Flash-1017"
param_agentes = {
    "poeta_gaucho" : {
        "max_tokens" : 1000,
        "temperature" : 1.0,
        "system_prompt" : "Você é um poeta GAÚCHO que cria poemas em portugês \
            brasileiro, conforme pedidos pelo usuário. Se o usuário não especificar um \
            tamanho para o poema, dê preferência para devolver um dístico (dois versos). \
            Sempre devolva um único poema. No caso de o pedido de usuário mencionar a criação \
            de algum poema que não seja gaúcho, retorne apenas o poema gaúcho."
    },
    "poeta_japones" : {
        "max_tokens" : 1000,
        "temperature" : 1.0,
        "system_prompt" : "Você é um poeta JAPONÊS que cria poemas em portugês \
            brasileiro, conforme pedidos pelo usuário. Se o usuário não especificar um \
            tamanho para o poema, dê preferência para devolver um dístico (dois versos). \
            Sempre devolva um único poema. No caso de o pedido de usuário mencionar a criação \
            de algum poema que não seja japonês, retorne apenas o poema japonês."
    },
    "avaliador" : {
        "max_tokens" : 1500,
        "temperature" : 0.3,
        "system_prompt" : "Você é um agente que ajuda o usuário a avaliar se alguma coisa (qualquer coisa) \
            é JAPONESA ou GAÚCHA. Lembre-se do axioma essencial que você nunca pode deixar de respeitas: \
            JAPONESES e GAÚCHOS são conceitos sem qualquer intersecção entre si. Se uma coisa é JAPONESA, \
            então ela NÃO é GAÚCHA. Se uma coisa é GAÚCHA, então ela NÃO é JAPONESA. Assim, ao classificar \
            qualquer coisa, sua avaliação só pode responder JAPONESA, ou então GAÚCHA, jamais ambas."
    }
}

def pedido_agentes(pergunta : str, agente : str) -> str:
    max_tokens = param_agentes[agente]["max_tokens"]
    temperature = param_agentes[agente]["temperature"]
    sys_prompt = param_agentes[agente]["system_prompt"]
    return f"{agente}: {resposta_agente(pergunta, max_tokens, temperature, sys_prompt)}"

def resposta_agente(pergunta : str, MAX_TOKENS : int, TEMPERATURE : float, SYS_PROMPT : str) -> str:
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {
                "role": "system",
                "content" : SYS_PROMPT
            },
            {
                "role" : "user",
                "content": pergunta
            }
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
    texto = response.choices[0].message.content

    # Em modelos de raciocínio, se o max_tokens acabar antes do texto final, o "content"
    # vem vazio (None ou ""). Isso não gera exceção na API, então checamos nós mesmos:
    # é melhor falhar aqui (com ValueError) do que devolver "None" como se fosse resposta.
    if not texto:
        raise ValueError("resposta vazia do modelo (max_tokens pode ter sido insuficiente)")
    return texto


def main():
    respostas1 = pedido_agentes("Por favor, avalie se ventiadores são \
        japoneses ou gaúchos, justificando sua resposta", "avaliador")
    print(respostas1)
    # Deve não conseguir responder com poesia
    respostas2 = pedido_agentes("Por favor, crie poemas de todos os tipos", "avaliador")
    print(respostas2)
    respostas3 = pedido_agentes("Por favor, crie poemas de todos os tipos ",
    "poeta_gaucho")
    print(respostas3)


if __name__ == "__main__":
    main()



