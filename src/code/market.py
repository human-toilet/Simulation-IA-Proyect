#dependencias
from src.code.company import Factory
from src.code.product import RawMaterial, RawMaterialMount
from src.code.sale import tec_factory, tec_raw, transport_factory, transport_raw
from src.utils import pen

#venta
class Sale: 
  def __init__(self, clasification: str, factories: list[Factory], materials: list[RawMaterial]) -> None:
    self._clasification = clasification
    self._factories = factories
    self._materials = materials
    
  @property
  def clasification(self) -> str:
    return self._clasification
  
  @property
  def factories(self) -> list[Factory]:
    return self._factories
  
  @property
  def materials(self) -> list[RawMaterial]:
    return self._materials

#mercado
class Market:  
  def __init__(self):
    self._tec = self._gen(tec_raw, tec_factory, 'tecnology')
    self._transport = self._gen(transport_raw, transport_factory, 'transport')
    self._products = [self._tec, self._transport]
    
  #generar los RawMaterialMount con una penalizacion aleatoria  
  def _gen(self, list_raw: list[RawMaterialMount], factories: list[Factory], clasification: str) -> Sale:
    raw = list(map(lambda x: RawMaterialMount(x.material, int(x.mount * pen())), list_raw))
    return Sale(clasification, factories, raw)
  
  @property
  def products(self) -> list[Sale]:
    return self._products
  