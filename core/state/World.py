from .Layer import Layer
from ..constants import CellValue
class World:
    def __init__(self, input_width : int, input_height : int):
        # size of our world. Should be immutable.
        self.__width = input_width
        self.__height = input_height
        
        # Initialize a dictionary of layers with default cell values
        self.__layers = {
            "ground": Layer(input_width, input_height, CellValue.GROUND_SEA),
            "impassable": Layer(input_width, input_height, CellValue.NONE),
            "objects": Layer(input_width, input_height, CellValue.NONE)
        }

    # Getter properties
    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def ground(self) -> Layer:
        return self.__layers["ground"]
    
    @property
    def impassable(self) -> Layer:
        return self.__layers["impassable"]
    
    @property
    def objects(self) -> Layer:
        return self.__layers["objects"]

    # Getter for a single layer
    def getLayer(self, name: str) -> Layer:
        if name not in self.__layers:
            raise ValueError(f"Layer {name} not found")

        return self.__layers[name]
    
    # Getters for all layers' names and values
    @property
    def layerNames(self) -> list[str]:
        return list(self.__layers.keys())

    @property
    def layers(self) -> list[Layer]:
        return list(self.__layers.values())