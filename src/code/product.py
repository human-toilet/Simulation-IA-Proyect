#producto
class Product:
  def __init__(self, name: str, clasification: str, price: int):
    self._name = name #nombre del producto
    self._clasification = clasification #clasificacion del producto
    self._price = price #precio por unidad
    
  def __eq__(self, product: object) -> bool:
    return self._name == product.name
    
  def __repr__(self) -> str:
    return f'Product: ({self._name}, {self._clasification})'
  
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def clasification(self) -> str:
    return self._clasification
  
  @property
  def price(self):
    return self._price
  
#materia prima
class RawMaterial:
  def __init__(self, name: str, product: Product, price: int):
    self._name = name #nombre de la materia prima
    self._product = product #producto que produce
    self._price = price #precio por unidad
  
  def __eq__(self, product: object) -> bool:
    return self._name == product.name
  
  def __repr__(self) -> str:
    return f'Raw material: ({self._name}, {self._product})'
  
  @property
  def price(self):
    return self._price
  
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def product(self) -> Product:
    return self._product
   
#cantidad de productos por unidad
class ProductMount:
  def __init__(self, product: Product, mount: int):
    self._product = product #producto que maneja
    self._mount = mount #cantidad de unidades del producto
    
  def __repr__(self) -> str:
    return f'({self._product}, {self._mount} units)'
  
  @property
  def product(self) -> Product:
    return self._product
   
  @property
  def mount(self) -> int:
    return self._mount
  
#cantidad de materia prima por unidad
class RawMaterialMount:
  def __init__(self, material: RawMaterial, mount: int):
    self._material = material #material prima que maneja que maneja
    self._mount = mount #cantidad de unidades del producto
  
  def __repr__(self) -> str:
    return f'({self._material}, {self._mount} units)'
    
  @property
  def material(self) -> RawMaterial:
    return self._material
   
  @property
  def mount(self) -> int:
    return self._mount


