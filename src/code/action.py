#dependencias
from src.code.product import *

#estado de los "ProductMount"
class State:
  def __init__(self, product_mount: list[ProductMount], scores: dict[Product, float]):
    self._product_mount = product_mount
    self._scores = self._set_scores(scores) if len(scores) != 0 else 0
    
  #puntuacion de un "State"
  def _set_scores(self, scores: dict[Product, float]) -> float:
    result = 0
    
    for products in self._product_mount:
      result += scores[products.product] * products.mount
      
    return result
  
  @property  
  def product_mount(self) -> list[ProductMount]:
    return self._product_mount

  @property
  def score(self) -> float:
    return self._scores
    
#acciones de una empresas
class Action:
  def __init__(self, transactions: list[ProductMount], products: list[ProductMount], market_products: list[RawMaterialMount]):
    self._products_score = self._score_products(transactions, products)
    self._products_limit = self._limits(products)
    self._states = self._gen_states(products, market_products)
  
  #puntuar los productos 
  def _score_products(self, transactions: list[ProductMount], products: list[ProductMount]) -> dict[Product, float]:
    result = {}
    
    for product_mount in products:
      aux = product_mount.product
      result[aux] = 0
      
      for transaction in transactions:
        if transaction.product == aux:
          result[aux] = transaction.mount / product_mount.mount 
          break
    
    return result
  
  #fijar el limite de cada producto para la generacion de "states" 
  def _limits(self, products: list[ProductMount]) -> dict[Product, float]:
    result = {}

    for product in products:
      aux = product.product
      result[aux] = product.mount + product.mount * self._products_score[aux]
      
    return result
  
  #generar estados
  def _gen_states(self, products: list[ProductMount], market: list[RawMaterialMount]) -> list[State]:
    result = []
    self._gen_states_rec(products, 0, [], result)
    
    if len(result) != 0:
      result.sort(key=lambda x: x.score)
    
    else:
      products = []
      
      for material_mount in market:
        products.append(ProductMount(material_mount.material.product, (material_mount.mount / 10) / 10))
      
      result.append(State(products, self._products_score))
      
    return result
    
  def _gen_states_rec(self, products: list[ProductMount], iter: int, temp: list[ProductMount], result: list[State]):
    if iter == len(products):
      if len(temp) != 0:
        result.append(State(temp, self._products_score))
    
    else:
      i = 0
      aux = products[iter]

      while True:  
        if i * 10 > self._products_limit[aux]:
          break
        
        self._gen_states_rec(products, iter + 1, temp + [ProductMount(products[iter].product, i * 10) if i != 0 else temp], result)
        i += 1
  
  @property
  def states(self) -> list[State]:
    return self._states
  