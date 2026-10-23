# Aqui guardamos modelos que devem ser validados com pydantic

from typing import Literal
from pydantic import BaseModel, Field, ValidationError
import json

class Rota(BaseModel):
    agentes : list[Literal["poeta_sulista","poeta_japones","avaliar_coisas"]] = Field(
        max_length=3, #No máximo, as 3 opções
        description="""Um agente escreve poesia sulista, um agente escreve poesia japonesa e um agente pode 
        avaliar se uma coisa qualquer é japonesa ou sulista"""
    )

# # Testes
# texto = '{"agentes": ["poeta_sulista", "poeta_japones"]}'
# rota = Rota.model_validate_json(texto)
# rota_json = Rota.model_json_schema(texto)
# print(rota)
# print("\n#====================================# \n")
# print(rota_json)
# print(json.dumps(Rota.model_json_schema(), indent=2))
# print(Rota.model_fields)
