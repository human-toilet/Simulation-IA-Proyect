from src.code.company import Company
from src.code.product import ProductMount
from src.utils import pen
import os

#cliente final que compra los productos a las empresas
class Client:
  def __init__(self, clasification: str):
    self._pen = self._get_pen(clasification)
    
  #calcular la penalizacion que usa el cliente para com[rar una cantidad de productos]
  def _get_pen(self, clasification='') -> float:
    if clasification == 'abundance':
      return pen(0.4)
    
    if clasification == 'low':
      return pen(max=0.3)
    
    return pen()
  
  #accion de comprar
  def buy(self, companies: list[Company]):
    for company in companies:
      for products in company.products:
        company.sell(ProductMount(products.product, int(products.mount * self._pen)))

#simulacion
class Sim():
  def __init__(self):
    self._companies: list[Company] = []
    self._client = None
    self._weeks = None
  
  #visual
  def sim(self):
    os.system('clear')
    input('Welcome. Before start, add a company')
    
    while True:
      name = self._set_name()
      clasification = self._set_clasification()
      self._companies.append(Company(name, clasification))
      os.system('clear')
      advance = input('Press "add" to add another company in other case press "enter" to continue:\n')
      
      if advance.lower().strip() != 'add':
        break
      
    self._client = self._set_client()
    self._weeks = self._set_weeks()
  
  #seleccionar el nombre de la empresa
  def _set_name(self) -> str:
    while True:
      os.system('clear')
      print('Add a name')
      name = input('Name: ')
      
      if len(list(filter(lambda x: x.name == name, self._companies))) != 0 or name == '':
        input('Invalid name or name already exists. Press "enter" to continue')
        continue
      
      return name
  
  #clasificar la empresa     
  def _set_clasification(self) -> str:
    while True:
      os.system('clear')
      print('Add a clasification')
      print('1.Tecnology')
      print('2.Transport')
      response = input()

      try:
        if int(response) == 1:
          return 'Tecnology'

        if int(response) == 2:
          return 'Transport'

        input('Ingress a valid option')

      except:
        input('Ingress a number')
        
  #crear al client
  def _set_client(self) -> Client:
    while True:
      os.system('clear')
      print('Now, select a clasification for the client')
      print('1.Abundance')
      print('2.Low')
      print('3.Random')
      option = input()
      
      try:
        if int(option) == 1:
          return Client('abundance')
        
        if int(option) == 2:
          return Client('low')
        
        if int(option) == 3:
          return(Client())
        
        input('Ingress a valid option. Press "enter" to continue')
        
      except:
        input('Ingress a number. Press "enter" to continue')
        
  #determinar la duracion en semanas de la simulacion
  def _set_weeks(self) -> int:
    while True:
      os.system('clear')
      print('Excelent. To finish, set the number of weeks that will take the simulation')
      weeks = input('Weeks: ')
      
      try:
        if int(weeks) > 0:
          return weeks

        input('Ingress a valid number. Press "enter" to continue')
        
      except:
        input('Ingress a valid number. Press "enter" to continue')
        