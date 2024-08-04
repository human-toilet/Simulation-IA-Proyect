#dependencias
from openai import OpenAI
from src.nlp.prompt import *
from src.utils import parse_json 

#respuesta del modelo a la query ingresada por el usuario
def response_result(sim: str, query: str) -> str:
  #cargar el server local
  client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

  completion = client.chat.completions.create(
    model="NousResearch/Hermes-2-Pro-Mistral-7B-GGUF",
    messages=[
      {"role": "system", "content": SYSTEM_PROMPT},
      {"role": "user", "content": build_prompt(sim, query)}
    ],
    temperature=0.7,
  )

  return parse_json(completion.choices[0].message.content)['result'] #respuesta en formato json
