"""
    Modelos que devem ser validados com pydantic
    Tipo: projeto
"""

from typing import Literal
from pydantic import BaseModel, Field

class Rota(BaseModel):
    lista_agentes : list[Literal["poeta_gaucho","poeta_japones","avaliador"]] = Field(
        max_length=3, #No máximo, as 3 opções
        description="""Um agente escreve poesia gaúcha, um agente escreve poesia japonesa e um agente pode 
        avaliar se uma coisa qualquer é japonesa ou gaúcha"""
    )


