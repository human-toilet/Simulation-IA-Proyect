#dependencias
from src.code.company import Company
from src.code.market import Market
from src.code.product import ProductMount
from src.nlp.nlp import response_result
from src.utils import pen
import os

#cliente final que compra los productos a las empresas
class Client:
  def __init__(self, companies: list[Company], clasification=None):
    self._pen = self._get_pen(clasification)
    self._last_week_transactions = {}
    
    for company in companies:
      self._last_week_transactions[company] = []
      
  #calcular la penalizacion que usa el cliente para com[rar una cantidad de productos]
  def _get_pen(self, clasification) -> float:
    if clasification == 'abundance':
      return pen(0.4)
    
    if clasification == 'low':
      return pen(max=0.2)
    
    return pen()
  
  #accion de comprar
  def action(self, companies: list[Company]):
    self._last_week_transactions = {}
    result = ''
    
    for company in companies:
      self.last_week_transactions[company] = []
      
      for products in company.products:
        company.sell(ProductMount(products.product, int(products.mount * self._pen)))
        result += f'El cliente compro {int(products.mount * self._pen)} unidades de {products.product}\n a la empresa {company.name}.\n'
        self._last_week_transactions[company].append(ProductMount(products.product, int(products.mount * self._pen)))
    
    return result
  
  @property
  def last_week_transactions(self) -> dict[Company, list[ProductMount]]:
    return self._last_week_transactions
       
#simulacion
class Sim():
  def __init__(self):
    self._companies = []
    self._client = None
    self._weeks = None
    self._market = Market()
  
  #visual
  def sim(self):
    os.system('clear')
    input('Welcome. Before start, add a company...')
    
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
    actions = self._execution()
    self._handle_querys(actions)
  
  #seleccionar el nombre de la empresa
  def _set_name(self) -> str:
    while True:
      os.system('clear')
      print('Add a name')
      name = input('Name: ')
      
      if len(list(filter(lambda x: x.name == name, self._companies))) != 0 or name == '':
        input('Invalid name or name already exists. Press "enter" to continue...')
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

        input('Ingress a valid option...')

      except:
        input('Ingress a number...')
        
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
          return Client(self._companies, 'abundance')
        
        if int(option) == 2:
          return Client(self._companies, 'low')
        
        if int(option) == 3:
          return Client(self._companies, )
        
        input('Ingress a valid option. Press "enter" to continue...')
        
      except:
        input('Ingress a number. Press "enter" to continue...')
        
  #determinar la duracion en semanas de la simulacion
  def _set_weeks(self) -> int:
    while True:
      os.system('clear')
      print('Excelent. To finish, set the number of weeks that will take the simulation')
      weeks = input('Weeks: ')
      
      try:
        if int(weeks) > 0:
          return int(weeks)

        input('Ingress number higher than 0. Press "enter" to continue')
        
      except:
        input('Ingress a valid number. Press "enter" to continue')
    
  #ejecutar la simulacion
  def _execution(self) -> str:
    os.system('clear')
    result = ''
    
    for i in range(self._weeks):
      result += f'SEMANA {i + 1}:\n'
      
      for company in self._companies:
        for sale in self._market.products:
          if sale.clasification.lower() == company.clasification.lower():
            result += f'{company.action(sale.materials, sale.factories, self._client.last_week_transactions[company])}.\n'
            break
        
      result += self._client.action(self._companies)
      result += '=============================================================================\n'
      
    input(result)
    return result
        
  #encabezado del informe que se le enviara al modelo
  def _header_inform(self) -> str:
    result = f'En la simulacion se encuentran las siguiente empresas:\n'
    
    for company in self._companies:
      result += f'Empresa "{company.name}", dedicada a {company.clasification} con un presupuesto de {company._presp} dolares\n'
      
    result += 'Tambien se cuenta con un cliente final, cuya labor es comprar los productos de la empresa.'
    result += 'A continuacion te voy a enviar un informe de lo que sucedio cada semana.\n'
    return result
    
  #manejo de las querys
  def _handle_querys(self, inform: str):
    os.system('clear')
    inform = self._header_inform() + inform
    input('Now, put some querys about the simulation...\n')
    
    while(True):  
      query = input('query: ')
      os.system('clear')
      print('Loading...')
      result = response_result(inform, query)
      os.system('clear')
      print('RESULTS:')
      print(result)
      print('')
      input('Press "enter" to make another query...\n')
