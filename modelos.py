# Aqui guardamos modelos que devem ser validados com pydantic

from typing import Literal
from pydantic import BaseModel, Field

class Rota(BaseModel):
    lista_agentes : list[Literal["poeta_gaucho","poeta_japones","avaliador"]] = Field(
        max_length=3, #No máximo, as 3 opções
        description="""Um agente escreve poesia gaúcha, um agente escreve poesia japonesa e um agente pode 
        avaliar se uma coisa qualquer é japonesa ou gaúcha"""
    )

# Testes 
# texto = '{"agentes": ["poeta_gaucho", "poeta_japones"]}'
# rota = Rota.model_validate_json(texto)
# rota_json = Rota.model_json_schema(texto)
# print(rota)
# print("\n#====================================# \n")
# print(rota_json)
# print(json.dumps(Rota.model_json_schema(), indent=2))
# print(Rota.model_fields)
# print



