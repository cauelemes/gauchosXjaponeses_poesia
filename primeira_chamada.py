import os
from dotenv import load_dotenv
from together import Together

load_dotenv()
client = Together() # Se a variável com chave API não existir, cliente falha na criação

prompt_entrada = input("Seu prompt: ")
print("Enviando pergunta ao modelo de temperatura alta ...")

# Primeira pergunta para modelos
response_temp_alta = client.chat.completions.create(
    model="zai-org/GLM-5.3-Flash",
    messages=[
        {
            "role": "system",
            "content" :  """Você é um assistente que fala em português brasileiro,
            feito para esclarecer as pessoas sobre  como o mundo é particionado entre 
            tudo o que é Gaúcho, e tudo o que é Japonês. Não existe intersecção,
            JAMAIS! Se uma coisa é gaúcha, então ela não é japonesa. E se uma coisa
            é japonesa, então ela não é gaúcha. Nunca permita que sua resposta vá contra
            este conhecimento basal, este axioma. Você também deve classificar coisas como
            gaúchas ou então como japonesas sempre que necessário. """
        },
        {
            "role" : "user",
            "content": prompt_entrada
        }
    ],
    temperature=0.9,
    max_tokens=1000,
)

print("Enviando pergunta ao modelo de temperatura baixa ...")
response_temp_baixa = client.chat.completions.create(
    model="zai-org/GLM-5.3-Flash",
    messages=[
        {
            "role": "system",
            "content" :  """Você é um assistente que fala em português brasileiro,
            feito para esclarecer as pessoas sobre  como o mundo é particionado entre 
            tudo o que é Gaúcho, e tudo o que é Japonês. Não existe intersecção,
            JAMAIS! Se uma coisa é gaúcha, então ela não é japonesa. E se uma coisa
            é japonesa, então ela não é gaúcha. Nunca permita que sua resposta vá contra
            este conhecimento basal, este axioma. Você também deve classificar coisas como
            gaúchas ou então como japonesas sempre que necessário. """
        },
        {
            "role" : "user",
            "content": prompt_entrada
        }
    ],
    temperature=0.1,
    max_tokens=1000,
)

# Obtendo a resposta textual e os tokens usados
texto_temp_alta = response_temp_alta.choices[0].message.content
tokens_temp_alta = response_temp_alta.usage
texto_temp_baixa = response_temp_baixa.choices[0].message.content
tokens_temp_baixa = response_temp_baixa.usage
print("Resposta do modelo com temperatura alta:\n  ", texto_temp_alta)
print("Quantidade de tokens gastos:\n  ", tokens_temp_alta, "\n")
print("Resposta do modelo com temperatura baixa:\n  ", texto_temp_baixa)
print("Quantidade de tokens gastos:", tokens_temp_baixa, "\n")

