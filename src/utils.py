#dependencias
import json
import random as rnd

#penalizacion
def pen(min=0, max=1) -> float:
  while True:
    response = rnd.random()
    
    if response > 0 and response <= max:
      return response
    
#respuesta parseada
def parse_json(json_data: str) -> dict:
  result = json.loads(json_data) #parsear de json a dict
  return result