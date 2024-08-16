#dependencias
from src.code.product import *

#estado de los "ProductMount"
class State:
  def __init__(self, product_mount: list[ProductMount], scores: dict[Product, float]):
    self._product_mount = product_mount
    self._scores = scores
    
  #puntuacion de un "State"
  def _score(self):
    result = 0
    
    for products in self._product_mount:
      result += self._scores[products.product] * products.mount
      
    return result
  
  @property  
  def product_mount(self) -> list[ProductMount]:
    return self._product_mount

  @property
  def score(self) -> float:
    return self._score()
    
#acciones de una empresas
class Action:
  def __init__(self, transactions: list[ProductMount], products: list[ProductMount]):
    self._products_score = self._score_products(transactions, products)
    self._products_limit = self._limits(products)
  
  #puntuar los productos 
  def _score_products(transactions: list[ProductMount], products: list[ProductMount]) -> dict[Product, float]:
    result = {}
    
    for product_mount in products:
      aux = product_mount.product
      result[aux] = 0
      
      for transaction in transactions:
        if transaction.product == aux:
          result[aux] = product_mount.mount / transaction.mount
          break
    
    return result
  
  #fijar el limite de cada producto para la generacion de "states" 
  def _limits(self, products: list[ProductMount]) -> dict[Product, float]:
    result = {}

    for product in products:
      aux = product.product
      result[aux] = product.mount
      
    return result