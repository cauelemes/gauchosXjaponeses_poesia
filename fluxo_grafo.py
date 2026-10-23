from typing import TypedDict, Annotated, Literal
from operator import add
from langgraph.graph import StateGraph, START, END

# Regular Expressions: para analisar textos nos nós "falsos" 
import re 

class State(TypedDict):
    pergunta: str
    respostas : Annotated[list[str], add] 

# Nós do grafo
def poeta_japones(state: State) -> dict:
    return {"respostas" : ["Eu escrevo poemas japoneses"] }

def poeta_gaucho(state: State) -> dict:
    return {"respostas" : ["Eu escrevo poemas gaúchos"] }

def avaliador(state: State) -> dict:
    return {"respostas" : ["Eu avalio se algo é japonês, ou então se é gaúcho"] }

def rotear(state: State) -> list[Literal["poeta_japones", "poeta_gaucho", "avaliador"]]:
    texto = state["pergunta"].lower()
    destinos = []

    if re.search(r"aval|classif|entend", texto):
        destinos.append("avaliador")
    elif re.search(r"poem|poes|poet", texto):
        if re.search(r"jap|nipo", texto):
            destinos.append("poeta_japones")
        if re.search(r"gauch|gaúch|sul", texto):
            destinos.append("poeta_gaucho")

    return destinos or ["avaliador"] # Retorna avaliador na dúvida

def main():

    # Construindo grafo
    builder = StateGraph(State)

    builder.add_node("poeta_japones", poeta_japones)
    builder.add_node("poeta_gaucho", poeta_gaucho)
    builder.add_node("avaliador", avaliador)
    builder.add_edge("poeta_japones", END)
    builder.add_edge("poeta_gaucho", END)
    builder.add_edge("avaliador", END)

    path_map = ["poeta_japones", "poeta_gaucho", "avaliador"]
    builder.add_conditional_edges(START, rotear, path_map=path_map)

    graph = builder.compile()

    # print(graph.get_graph().draw_mermaid())

    # Executando grafo
    result1 = graph.invoke(
        {
            "pergunta"  : "escreva um poema japonês?",
            "respostas" : []
        }
    )
    print(result1)

    result2 = graph.invoke(
        {
            "pergunta"  : "me dê um poema gaúcho?",
            "respostas" : []
        }
    )
    print(result2)

    result3 = graph.invoke(
        {
            "pergunta"  : "avalie se essa coisa é japonesa ou gaucha, por favor?",
            "respostas" : []
        }
    )
    print(result3)

    result4 = graph.invoke(
        {
            "pergunta"  : "escreva um poema japones e um gaucho?",
            "respostas" : []
        }
    )
    print(result4)

    st_inicial = {
        "pergunta"  : "avalie se essa coisa é japonesa ou gaucha, por favor?",
        "respostas" : []
    }
    print("Resultado passo a passo:")
    for passo in graph.stream(st_inicial, stream_mode="updates"):
        # Cada item é {nome_do_no: atualização_que_ele_devolveu}.
        print("  ", passo)


    print(graph.get_graph().draw_ascii())
    return

main()