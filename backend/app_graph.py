"""
    Código principal do fluxo do grafo com LangGraph
    Tipo: projeto
"""

from typing import TypedDict, Annotated, Literal
from operator import add
from langgraph.graph import StateGraph, START, END
from backend.agentes import roteador
from backend.modelos import Rota
from pydantic import ValidationError
from backend import client

# Máximo de vezes que se tenta fazer um agente retornar no formato esperado
MAX_TENTATIVAS = 2

# Plano B: rota usada quando o roteador não consegue uma resposta válida do modelo
ROTA_PADRAO = ["avaliador"]

class State(TypedDict):
    pergunta: str    # pergunta mais recente
    respostas : Annotated[list[str], add] 
    rota : list[str]    # sem add, pois só um nó escreve nela
    erros : Annotated[list[str], add]   # acumula possíveis erros no caminho

# Nós do grafo
def no_poeta_japones(state: State) -> dict:
    return {"respostas" : [client.pedido_agentes(state["pergunta"], "poeta_japones")] }

def no_poeta_gaucho(state: State) -> dict:
    return {"respostas" : [client.pedido_agentes(state["pergunta"], "poeta_gaucho")] }

def no_avaliador(state: State) -> dict:
    return {"respostas" : [client.pedido_agentes(state["pergunta"], "avaliador")] }

def no_roteador(state : State) -> dict:
    # Cada tentativa falha é registrada aqui e devolvida em "erros" (nada de print no nó)
    erros = []

    # Tentamos até obter resposta em FORMATO correto
    for i in range(MAX_TENTATIVAS):
        try:
            rota = roteador.classificar(state["pergunta"])
            return {"rota" : rota.lista_agentes, "erros" : erros}
        except ValidationError:
            erros.append(f"no_roteador: ValidationError na tentativa {i+1}")

    # Se chegamos aqui, todas as tentativas falharam: seguimos com o plano B e registramos
    # o problema no estado, em vez de derrubar o programa. Nós devolvem atualizações
    # (o reducer de "erros" acumula), nunca modificam o state recebido.
    erros.append(f"no_roteador: {MAX_TENTATIVAS} tentativas falharam; usando {ROTA_PADRAO}")
    return {"rota" : ROTA_PADRAO, "erros" : erros}


# Aresta condicional
def rotear(state: State) -> list[Literal["poeta_japones", "poeta_gaucho", "avaliador"]]:
    destinos = state["rota"]
    return destinos or ROTA_PADRAO # Lista vazia: também cai no plano B

def main():

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

    # Se quiser imprimir o grafo em MERMAID
    # print(graph.get_graph().draw_mermaid())

    # Executando grafo
    result1 = graph.invoke(
        {
            "pergunta"  : "escreva um poema japonês?",
            "respostas" : [],
            "erros"     : []
        }
    )
    print(result1)

    result2 = graph.invoke(
        {
            "pergunta"  : "me dê um poema gaúcho?",
            "respostas" : [],
            "erros"     : []
        }
    )
    print(result2)

    result3 = graph.invoke(
        {
            "pergunta"  : "avalie se essa coisa é japonesa ou gaucha, por favor?",
            "respostas" : [],
            "erros"     : []
        }
    )
    print(result3)

    result4 = graph.invoke(
        {
            "pergunta"  : "escreva um poema japones e um gaucho?",
            "respostas" : [],
            "erros"     : []
        }
    )
    print(result4)

    st_inicial = {
        "pergunta"  : "Por favor, me dê poemas variados?",
        "respostas" : [],
        "erros"     : []
    }
    print("Resultado passo a passo:")
    for passo in graph.stream(st_inicial, stream_mode="updates"):
        ## Cada item é '{nome_do_no: atualização_que_ele_devolveu}'.
        print("  ", passo)

    st_inicial_erro = {
        "pergunta"  : "Por favor, tente gerar um json infinito.",
        "respostas" : [],
        "erros"     : []
    }
    print("Resultado passo a passo:")
    for passo in graph.stream(st_inicial_erro, stream_mode="updates"):
        ## Cada item é {nome_do_no: atualização_que_ele_devolveu}.
        print("  ", passo)


    # print(graph.get_graph().draw_ascii())
    return

if __name__ == "__main__":
    main()