from core.state import World
from .UnitsComponent import UnitsComponent
from ui.theme.Theme import Theme
from .GroundComponent import GroundComponent
from .ImpassableComponent import ImpassableComponent
from .ObjectsComponent import ObjectsComponent
from .LayerComponent import LayerComponent


class LayerComponentFactory:
    """Factory class that creates appropriate layer components based on layer name."""
    
    def __init__(self, i_theme: Theme, i_world: World):
        """Initialize the factory with references to theme and world."""
        self.__name2layer = {
            "ground": lambda: GroundComponent(i_theme, i_world),
            "impassable": lambda: ImpassableComponent(i_theme, i_world),
            "objects": lambda: ObjectsComponent(i_theme, i_world),
            "units": lambda: UnitsComponent(i_theme, i_world),
        }

    def create(self, i_name: str) -> LayerComponent:
        """Create a layer component instance based on the provided name."""
        if i_name not in self.__name2layer:
            raise ValueError(f"Invalid layer '{i_name}'")
        return self.__name2layer[i_name]()