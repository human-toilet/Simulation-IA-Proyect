#dependencias
from src.code.product import *
from src.utils import pen

#estado de los "ProductMount"
class State:
  def __init__(self, product_mount: list[ProductMount], scores: dict[Product, float]):
    self._product_mount = product_mount
    self._scores = self._set_scores(scores) if len(scores) != 0 else 0
    
  #puntuacion de un "State"
  def _set_scores(self, scores: dict[Product, float]) -> float:
    result = 0
    total = 0
    
    for products in self._product_mount:
      result += scores[products.product] * products.mount
      total += products.mount
      
    return result /total
  
  @property  
  def product_mount(self) -> list[ProductMount]:
    return self._product_mount

  @property
  def score(self) -> float:
    return self._scores
    
#acciones de una empresas (IA)
class AStar:
  def __init__(self, transactions: list[ProductMount], products: list[ProductMount], market_products: list[ProductMount]):
    self._products_score = self._score_products(transactions, products) #puntuacion de cada producto en dependencia de lo que vendi respecto a lo que tenia
    self._products_limit = self._limits(products) #limite de cada producto
    self._states = self._gen_states(products, market_products) #generar los estados para la siguiente semana
  
  #puntuar los productos 
  def _score_products(self, transactions: list[ProductMount], products: list[ProductMount]) -> dict[Product, float]:
    result = {}
    
    for product_mount in products:
      aux = product_mount.product
      result[aux] = 0
      
      for transaction in transactions:
        if transaction.product.name == aux.name:
          result[aux] = transaction.mount / product_mount.mount 
          break
    
    return result
  
  #fijar el limite de cada producto para la generacion de "states" 
  def _limits(self, products: list[ProductMount]) -> dict[Product, int]:
    result = {}

    for product in products:
      aux = product.product
      result[aux] = product.mount + int(product.mount * self._products_score[aux])
      
    return result
  
  #generar estados
  def _gen_states(self, products: list[ProductMount], market: list[ProductMount]) -> list[State]:
    result = []
    self._gen_states_rec(products, 0, [], result)
    
    if len(result) == 0:
      products = []
      
      for product_mount in market:
        products.append(ProductMount(product_mount.product, int(product_mount.mount * pen(max=0.15))))
      
      result.append(State(products, self._products_score))
      
    return result
    
  def _gen_states_rec(self, products: list[ProductMount], iter: int, temp: list[ProductMount], result: list[State]):
    if iter == len(products):
      if len(temp) != 0:
        result.append(State(temp, self._products_score))
    
    else:
      i = 0
      aux = products[iter].product

      while True:  
        if i * 10 > self._products_limit[aux]:
          break
        
        self._gen_states_rec(products, iter + 1, temp + [ProductMount(products[iter].product, i * int(self._products_limit[aux] / 10) if self._products_limit[aux] > 10 else 1)] if i != 0 else temp, result)
        i += 1
  
  @property
  def states(self) -> list[State]:
    return self._states
  
#Nodo A*
class Node:
  def __init__(self, state: State, cost: float):
    self._product_mount = state.product_mount
    self._score = state.score - cost
    
  @property
  def product_mount(self) -> list[ProductMount]:
    return self._product_mount
  
  @property
  def score(self) -> float:
    return self._score
  
#agente BDI
class AgentBDI:
  def __init__(self, transactions: list[ProductMount], products: list[ProductMount], market_products: list[ProductMount],
               beliefs: list):
    self._agent = AStar(transactions, products, market_products) #agente A*
    pass
  
  #acciones del agente BDI
  def action(self) -> list[State]:
    return self._agent.states