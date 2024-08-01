#dependencias
from src.code.company import Factory
from src.code.product import Product, RawMaterial, RawMaterialMount

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

#apartado de tecnologia
celular = Product('celular', 'tecnology', 100)
computer = Product('computer', 'tecnology', 150)
tv = Product('tv', 'tecnology', 50)
raw_celular = RawMaterial('raw celular', celular, 10)
raw_computer = RawMaterial('raw computer', computer, 15)
raw_tv = RawMaterial('raw tv', tv, 5)
factory_celular = Factory(raw_celular)
factory_computer = Factory(raw_computer)
factory_tv = Factory(raw_tv)
tec_raw = [RawMaterialMount(raw_celular, 500), RawMaterialMount(raw_computer, 300), RawMaterialMount(raw_tv, 400)]
tec_factory = [factory_celular, factory_computer, factory_tv]

#apartado de transporte
car = Product('car', 'transport', 40000)
bike = Product('bike', 'transport', 2000)
truck = Product('truck', 'transport', 60000)
raw_car = RawMaterial('raw car', car, 1200)
raw_bike = RawMaterial('raw bike', bike, 200)
raw_truck = RawMaterial('raw truck', truck, 2000)
factory_car = Factory(raw_car)
factory_bike = Factory(raw_bike)
factory_truck = Factory(raw_truck)
transport_raw = [RawMaterialMount(raw_car, 100), RawMaterialMount(raw_bike, 200), RawMaterialMount(raw_truck, 50)]
transport_factory = [factory_car, factory_bike, factory_truck]

tec = Sale('tecnology', tec_factory, tec_raw)
transport = Sale('transport', transport_factory, transport_raw)


