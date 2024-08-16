#dependencias
from src.code.product import *
from src.utils import pen

#factoria
class Factory:
  def __init__(self, material: RawMaterial, price=100000):
    self._material = material #tipo de producto que produce
    self._price = price #precio de la factoria
    self._active = True #saber si la factoria esta o no en condiciones de usarse
    self._reparation = 0 if self._active else price * pen(max=0.25) #precio de arreglar la factoria
  
  def __repr__(self) -> str:
    return f'(Factory of: {self._material})'
  
  #producir en una cierta cantidad  
  def produce(self, cant: int) -> ProductMount:
    return ProductMount(Product(self._material.product.name, self.material.product.clasification, 
                                self.material.product.price + self.material.product.price / 3), cant)
   
  #arreglar la factoria
  def activate(self):
    self._active = True
   
  @property
  def material(self) -> RawMaterial:
    return self._material

  @property
  def price(self) -> int:
    return self._price 

  @property
  def active(self) -> bool:
    return self._active

  @property
  def reparation(self) -> float:
    return self._reparation
  
#empresa
class Company:
  def __init__(self, name: str, clasification: str, presp=10000000.0):
    self._name = name #nombre de la empresa
    self._clasification = clasification #tipo de producto al que se dedica
    self._presp = presp #presupuesto de la empresa
    self._factories: list[Factory] = [] #factorias que posee
    self._raw_material: list[RawMaterialMount] = [] #materia prima
    self._products: list[ProductMount] = [] #productos
    
  def __repr__(self) -> str:
    return f'({self._name}, {self._clasification})'  
  
  #factoria que produce un producto
  def _get_factory(self, material: RawMaterial) -> Factory:
    for factory in self._factories:
      if factory.material == material:
        return factory
  
  #agregar una cantidad de un producto
  def _add_product(self, product: ProductMount):
    for mount in self._products:
      if mount.product == product:
        mount.mount += product.mount
        return
    
    self._products.append(product)
   
  #agregar una cantidad de materia prima
  def _add_raw(self, raw: RawMaterialMount):
    for mount in self._raw_material:
      if mount.material == raw:
        mount.mount += raw.mount
        return
    
    self._products.append(raw)
   
  #eliminar un producto vendido 
  def _delete_product(self, product: ProductMount):
    for i in range(len(self._products)):
      if self._products[i].product == product:
        self._products[i].mount -= product.mount
        self._presp += self._products[i].product.price * self._products[i].mount
        
        if self._products[i].mount == 0:
          self._products = self._products[:i] + self._products[i + 1:] if i != len(self._products) - 1 else self._products[:i]
    
  #eliminar materia prima usada
  def _delete_raw(self, raw: RawMaterial, cant: int):
    for i in range(len(self._raw_material)):
      if self._raw_material[i].material == raw:
        self._raw_material[i].mount -= cant
        
        if self._raw_material[i] == 0:
          self._raw_material = self._raw_material[:i] + self._raw_material[i + 1:] if i != len(self._raw_material) - 1 else self._raw_material[:i]
          
  #producir un producto en cierta cantidad
  def _produce(self, raw: RawMaterial, cant: int) -> bool:
    factory = self._get_factory(raw)   
    production = factory.produce(cant)
    self._add_product(production)
    self._delete_raw(raw, cant * 10)
  
  #construir una factoria
  def _build(self, factories: list[Factory], raw: RawMaterial):
    for factory in factories:
      if factory.material == raw:
        self._factories.append(factory)
        self._presp -= factory.price
        return
  
  #comprar materia prima
  def _buy(self, materials: list[RawMaterialMount]):
    for raw in materials:
      self._presp -= raw.mount * raw.material.price
      self._add_raw(raw)
  
  #arreglar una factoria
  def _fix_factory(self, factory: Factory):
    factory.activate()
    self._presp -= factory.reparation
  
  #vender productos
  def sell(self, products: list[ProductMount]):
    for product in products:
      self._presp += product.mount * product.product.price
      self._delete_product(product)
  
  #accion de cada empresa (IA)
  def action(self, materials: list[RawMaterialMount], transactions: list[ProductMount]) -> str:
    return ''
  
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def clasification(self) -> str:
    return self._clasification
  
  @property
  def products(self) -> list[ProductMount]:
    return self._products
  
  @property
  def presp(self) -> float:
    return self._presp