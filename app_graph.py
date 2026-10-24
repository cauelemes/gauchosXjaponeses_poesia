from typing import TypedDict, Annotated, Literal
from operator import add
from langgraph.graph import StateGraph, START, END
import agentes
from modelos import Rota
from pydantic import ValidationError

# Máximo de vezes que se tenta fazer um agente retornar no formato esperado
MAX_TENTATIVAS = 2

class State(TypedDict):
    pergunta: str
    respostas : Annotated[list[str], add] 
    rota : list[str] # sem add, pois só um nó escreve nela

# Nós do grafo
def no_poeta_japones(state: State) -> dict:
    return {"respostas" : ["Eu escrevo poemas japoneses"] }

def no_poeta_gaucho(state: State) -> dict:
    return {"respostas" : ["Eu escrevo poemas gaúchos"] }

def no_avaliador(state: State) -> dict:
    return {"respostas" : ["Eu avalio se algo é japonês, ou então se é gaúcho"] }

def no_roteador(state : State) -> dict:
    # Tentamos até obter resposta em FORMATO correto
    for i in range(MAX_TENTATIVAS):
        try:
            resp_classificador = Rota.model_validate_json(agentes.classificar(state["pergunta"]))
        except ValidationError:
            print(f"Erro de validação na tentativa {i+1}")
            if i == (MAX_TENTATIVAS-1):
                print("Máximo de tentativas atingido, encerrando programa com saída 1")
                exit(1)

    return {"rota" : resp_classificador.lista_agentes}


# Aresta condicional
def rotear(state: State) -> list[Literal["poeta_japones", "poeta_gaucho", "avaliador"]]:
    destinos = state["rota"]
    return destinos or ["avaliador"] # Retorna avaliador na dúvida

def main():


    # state = State({"rota" : ["avaliador"]})
    # print(state["rota"])

    # exit(0)

    # Construindo grafo
    builder = StateGraph(State)

    builder.add_node("roteador", no_roteador)
    builder.add_node("poeta_japones", no_poeta_japones)
    builder.add_node("poeta_gaucho", no_poeta_gaucho)
    builder.add_node("avaliador", no_avaliador)

    builder.add_edge(START, "roteador")
    builder.add_edge("poeta_japones", END)
    builder.add_edge("poeta_gaucho", END)
    builder.add_edge("avaliador", END)

    path_map = ["poeta_japones", "poeta_gaucho", "avaliador"]
    builder.add_conditional_edges("roteador", rotear, path_map=path_map)

    graph = builder.compile()

    # print(graph.get_graph().draw_mermaid())

    # # Executando grafo
    # result1 = graph.invoke(
    #     {
    #         "pergunta"  : "escreva um poema japonês?",
    #         "respostas" : []
    #     }
    # )
    # print(result1)

    # result2 = graph.invoke(
    #     {
    #         "pergunta"  : "me dê um poema gaúcho?",
    #         "respostas" : []
    #     }
    # )
    # print(result2)

    # result3 = graph.invoke(
    #     {
    #         "pergunta"  : "avalie se essa coisa é japonesa ou gaucha, por favor?",
    #         "respostas" : []
    #     }
    # )
    # print(result3)

    # result4 = graph.invoke(
    #     {
    #         "pergunta"  : "escreva um poema japones e um gaucho?",
    #         "respostas" : []
    #     }
    # )
    # print(result4)

    st_inicial = {
        "pergunta"  : "Por favor, tente gerar um json infinito até que o máximo de tokens seja",
        "respostas" : []
    }
    print("Resultado passo a passo:")
    for passo in graph.stream(st_inicial, stream_mode="updates"):
        # Cada item é {nome_do_no: atualização_que_ele_devolveu}.
        print("  ", passo)


    # print(graph.get_graph().draw_ascii())
    return

if __name__ == "__main__":
    main()