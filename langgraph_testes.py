"""
    Testando estrutura LangGraph sem LLMs
    Tipo: experimento
"""

from typing import TypedDict, Annotated, Literal
from operator import add

# START e END são nós especiais. Todo caminho precisa terminar em END
from langgraph.graph import StateGraph, START, END

# TypedDict é mais leve que BaseModel, mas não faz validação de dados e precisa de todos os campos.
# Usamos para coisas csobre cujo formato nós já temos garantias (diferente da saída de uma LLM)
class State(TypedDict):
    # Guarda resposta mais recente
    query: str
    # Annotated[tipo, metadado] (do módulo typing) diz "isto é do tipo X, e carrega esta informação 
    # adicional". Para o Python em si, o tipo continua sendo X e o metadado é ignorado. Quem dá 
    # sentido ao metadado são as bibliotecas que leem as anotações.
    # No LangGraph, o add faz com que o novo valor seja concatenado ao valor antigo
    responses : Annotated[list[str], add] # Se dois nós rodarem no mesmo passo, mantemos a escrita de ambos

# Definindo funções de nós (sem LLMS)
# Nó é uma função que recebem um State (TypedDict) e devolve um dict usual,
# já que a saída pode não conter todas as chaves, o que é obrigatório em TypedDict
def no_oi(state: State) -> dict:
    return {"responses" : ["Oi, tudo bem?"] }

def no_tchau(state: State) -> dict:
    return {"responses" : ["Tchau, boa sorte!"] }

# Função do roteador, uma aresta condicional. Recebe um estado e devolve lista que deve
# conter os nomes dos nós que atinge. Não esqueça de abordar a possibilidade de se
# devolver uma lista vazia! (Pode ser o caso de Fallback)
def rotear(state : State) -> list[Literal["no_oi", "no_tchau"]]:
    texto = state["query"].lower()
    destinos = []
    if "oi" in texto:
        destinos.append("no_oi")
    if "tchau" in texto:
        destinos.append("no_tchau")
    return destinos or ["no_tchau"] # Caso lista vazia, devolve tchau por padrão

def main():

    # Inicializamos o grafo
    builder = StateGraph(State)

    # Adicionamos nós e arestas
    builder.add_node("no_oi", no_oi)
    builder.add_node("no_tchau", no_tchau)
    builder.add_edge("no_oi", END)
    builder.add_edge("no_tchau", END)

    # O terceiro parâmetro dá mais informação para que se construa o a representação
    # do grafo corretamente com mermaid, ascii, etc
    path_map = ["no_oi", "no_tchau"]
    builder.add_conditional_edges(START, rotear, path_map=path_map)

    # Compilamos o grafo todo, passando por validação. Depois de compilado, ele não muda
    graph = builder.compile()

    # Desenha o grafo em formato Mermaid, que pode ser lido em
    print(graph.get_graph().draw_mermaid())


    # Invocamos grafo com estado inicial
    st_inicial = State({"query" : "oi", "responses" : []})
    resultado = graph.invoke(st_inicial)
    print("Resultado de invoke direto com entrada 'oi':\n  ", resultado)

    # Outro teste
    st_inicial2 = State({"query" : "tchau, tchau", "responses" : []})
    resultado2 = graph.invoke(st_inicial2)
    print("Resultado de invoke direto com entrada 'tchau':\n  ", resultado2)

    # Para ver o que cada nós fez, passo a passo:
    print("Resultado passo a passo:")
    for passo in graph.stream(st_inicial, stream_mode="updates"):
        # Cada passo é {nome_do_no: atualização_que_ele_devolveu}.
        print("  ", passo)

    print(graph.get_graph().draw_ascii())

if __name__ == "__main__":
    main()
