#dependencias
from src.code.action import Action
from src.code.product import *
from src.utils import pen, clone

#factoria
class Factory:
  def __init__(self, material: RawMaterial, price=100000.0):
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
    activation = True if pen() >= 0.15 else False
    self._active = activation
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
    self._factories = [] #factorias que posee
    self._raw_material = [] #materia prima
    self._products = [] #productos
    self._last_products = [] #productos de la semana anterior
    
  def __repr__(self) -> str:
    return f'({self._name}, {self._clasification})'  
  
  #factoria que produce un producto
  def _get_factory(self, material: RawMaterial) -> Factory:
    for factory in self._factories:
      if factory.material == material:
        return factory
  
  #materia prima que produce un producto
  def _get_material(self, product: Product) -> RawMaterial:
    for materials in self._raw_material:
      if materials.material.product.name == product.name:
        return materials.material
  
  #agregar una cantidad de un producto
  def _add_product(self, product: ProductMount):
    for i in range(len(self._products)):
      if self._products[i].product.name == product.product.name:
        self._products[i] = ProductMount(self._products[i].product, self._products[i].mount + product.mount)
        return
    
    self._products.append(product)
   
  #agregar una cantidad de materia prima
  def _add_raw(self, raw: RawMaterialMount):
    for i in range(len(self._raw_material)):
      if self._raw_material[i].material == raw.material:
        self._raw_material[i] = ProductMount(self._raw_material[i].material, self._raw_material[i].mount + raw.mount)
        return
    
    self._raw_material.append(raw)
   
  #eliminar un producto vendido 
  def _delete_product(self, product: ProductMount):
    for i in range(len(self._products)):
      if self._products[i].product.name == product.product.name:
        self._products[i] = ProductMount(self._products[i].product, self._products[i].mount - product.mount)
        self._presp += self._products[i].product.price * self._products[i].mount
        
        if self._products[i].mount == 0:
          self._products = self._products[:i] + self._products[i + 1:] if i != len(self._products) - 1 else self._products[:i]
    
  #eliminar materia prima usada
  def _delete_raw(self, raw: RawMaterial, cant: int):
    for i in range(len(self._raw_material)):
      if self._raw_material[i].material == raw:
        self._raw_material[i] = RawMaterialMount(self._raw_material[i].material, self._raw_material[i].mount - cant)
        
        if self._raw_material[i].mount == 0:
          self._raw_material = self._raw_material[:i] + self._raw_material[i + 1:] if i != len(self._raw_material) - 1 else self._raw_material[:i]
          
  #producir un producto en cierta cantidad
  def _produce(self, raw: RawMaterial, cant: int) -> bool:
    factory = self._get_factory(raw)  
    
    if not factory.active:
      self._fix_factory(factory)
       
    production = factory.produce(cant)
    self._add_product(production)
    self._delete_raw(raw, cant * 10)
  
  #construir una factoria
  def _build(self, factories: list[Factory], raw: RawMaterial) -> Factory:
    for factory in factories:
      if factory.material == raw:
        self._factories.append(factory)
        self._presp -= factory.price
        return factory
  
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
  def sell(self, products: ProductMount):
    self._presp += products.mount * products.product.price
    self._delete_product(products)
  
  #accion de cada empresa (IA)
  def action(self, materials: list[RawMaterialMount], factories: list[Factory], transactions: list[ProductMount]) -> str:
    action = Action(transactions, self._last_products, materials)
    states = action.states
    
    for state in states:
      if self._valid(state.product_mount) and self._action(state.product_mount, materials, factories, True):
        result = self._action(state.product_mount, materials, factories, False)
        self._last_products = clone(self._products)
        return result
  
  def _action(self, production: list[ProductMount], material_market: list[RawMaterialMount], 
              factories_market: list[Factory], clon: bool) -> str | bool:
    temp = self._clone_company() if clon else self
    inform = ''
    
    for products in production:
      rest = None
      
      for product_mount in temp.products:
        if product_mount.product.name == products.product.name:
          rest = products.mount - product_mount.mount
          break
      
      if rest == None:
        rest = products.mount
        
      for materials in material_market:
        if materials.material.product.name == products.product.name:
          temp._buy([RawMaterialMount(materials.material, rest * 10)])
          inform += f'La empresa {temp._name} compro {rest * 10} unidades de {materials.material.name} a {materials.material.price} dolares cada una.\n'
          break
        
      if temp._get_factory(temp._get_material(products.product)) == None:
        factory = temp._build(factories_market, temp._get_material(products.product))
        inform += f'La empresa {temp.name} construyo una factoria por el precio de {factory.price} dolares que convierte {temp._get_material(products.product).name} en {products.product.name}.\n'
        
      temp._produce(temp._get_material(products.product), rest)
      inform += f'La empresa {temp.name} produjo {rest} unidades de {products.product}.\n'
        
    if temp._presp >= 0:
      return inform
      
  #clonar una empresa
  def _clone_company(self) -> 'Company':
    clon = Company('clon', self._clasification, self._presp)
    clon._factories = clone(self._factories)
    clon._raw_material = clone(self._raw_material)
    clon._products = clone(self._products)
    return clon
  
  #saber si un estado es valido
  def _valid(self, state: list[ProductMount]) -> bool:
    for products in state:
      for product_mount in self._products:
        if products.product == product_mount.product and products.mount < product_mount.mount:
          return False
          
    return True
     
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def clasification(self) -> str:
    return self._clasification
  
  @property
  def products(self) -> list[ProductMount]:
    return self._products
  